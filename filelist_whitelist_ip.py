import requests
from bs4 import BeautifulSoup
from time import sleep
import logging
import random
import re
import os
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def is_ipv4_address(ip):
    return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip))


def authenticate(user, password):
    session = requests.Session()
    url = 'https://filelist.io/login.php'

    while True:
        try:
            response = session.get(url)
            break
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with {url}: {e}")
            sleep(600)  # 10 minutes before retrying

    soup = BeautifulSoup(response.content, "html.parser")
    validator = soup.find('input', {'name': 'validator'}).get('value', '') if soup.find('input',
                                                                                        {'name': 'validator'}) else ''
    data = {
        "validator": validator,
        "username": user,
        "password": password,
        "unlock": "1",
        "returnto": "%252F",
    }

    login_url = 'https://filelist.io/takelogin.php'

    while True:
        try:
            session.post(login_url, data=data)
            if not session.cookies.get("pass"):
                logging.error("Login not successful, check credentials...")
                logging.error("Will try again after 6 hours")
                # 6 hour wait because wrong credentials can block the account.
                sleep(21600)
            return session
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with {login_url}: {e}")
            sleep(600)  # 10 minutes before retrying


def get_current_wan_ip():
    urls = [
        'https://checkip.amazonaws.com/',
        'https://ipinfo.io/ip/',
        'https://api.ipify.org',
        'https://ifconfig.io/ip',
        'https://icanhazip.com/'
    ]

    # Randomising which endpoint is used to not abuse.
    random.shuffle(urls)

    while True:
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                logging.info(f"Got IP from {url}!")
                ip = response.text.strip()
                if is_ipv4_address(ip):
                    return ip  # Return if successful
                else:
                    logging.warning(f"IP format is wrong - {ip}")
            except requests.exceptions.RequestException as e:
                logging.warning(f"Error with {url}: {e}")

        logging.error("Cannot get WAN IP; possibly a connection issue, retrying in 5 minutes...")
        sleep(300)


def is_authenticated(session):
    profile_page_url = 'https://filelist.io/my.php'
    while True:
        try:
            response = session.get(profile_page_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check for the presence of the 'whitelistip' input field
            whitelist_ip_field = soup.find('input', {'name': 'whitelistip'})

            return whitelist_ip_field is not None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with {profile_page_url}: {e}")
        logging.error(f"Cannot get {profile_page_url}, retrying in 5 minutes...")
        sleep(300)


def fetch_profile_ip(session):
    my_page_url = "https://filelist.io/my.php"

    while True:
        try:
            response = session.get(my_page_url)
            soup = BeautifulSoup(response.content, "html.parser")

            whitelist_ip_field = soup.find('input', {'name': 'whitelistip'})
            profile_ip = whitelist_ip_field.get('value', '') if whitelist_ip_field else ''

            return profile_ip
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with {my_page_url}: {e}")
        logging.error(f"Cannot get {my_page_url}, retrying in 5 minutes...")
        sleep(300)


def fetch_and_update_profile(session, current_wan_ip):
    my_page_url = "https://filelist.io/my.php"
    update_page_url = "https://filelist.io/takeprofedit.php"

    while True:
        try:
            response = session.get(my_page_url)
            soup = BeautifulSoup(response.content, "html.parser")

            form_data = {}
            # Handle text inputs, radio buttons, and hidden inputs
            for input_tag in soup.find_all('input', type=['text', 'radio', 'password', 'hidden']):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                if input_tag.get('type') == 'radio' and not input_tag.has_attr('checked'):
                    continue
                if name:
                    form_data[name] = value

            # Handle checkboxes, include only if checked
            for checkbox in soup.find_all('input', type='checkbox'):
                name = checkbox.get('name')
                if name == 'resetpasskey':  # Skip adding resetpasskey to form_data
                    continue
                if checkbox.has_attr('checked'):
                    form_data[name] = 'on'

            # Handle select dropdowns
            for select in soup.find_all('select'):
                name = select.get('name')
                selected_option = select.find('option', selected=True)
                if selected_option:
                    form_data[name] = selected_option.get('value', '')

            # Update 'whitelistip' with the current WAN IP if it's different
            if form_data.get('whitelistip') != current_wan_ip:
                form_data['whitelistip'] = current_wan_ip

                # Submit the update request with all form data, excluding resetpasskey
                update_response = session.post(update_page_url, data=form_data)
                if update_response.status_code == 200:
                    logging.info("Successfully updated the whitelist IP.")
                    break
                else:
                    print(f"Failed to update. Status Code: {update_response.status_code}")
            else:
                logging.info("No update needed; WAN IP matches the Whitelist IP.")
                break
        except requests.exceptions.RequestException as e:
            logging.error(f"Error with updating whitelist IP: {e}")
        logging.info(f"Retrying in 5 minutes...")
        sleep(300)

def load_secret(path):
    try:
        with open(path, 'r') as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError as e:
        logging.error(e)

if __name__ == '__main__':
    username_path = os.environ.get('FL_USERNAME', None)
    password_path = os.environ.get('FL_PASSWORD', None)

    username = load_secret(username_path)
    password = load_secret(password_path)

    if username is None:
        logging.error("Error: FL_USERNAME is not set.")
        sys.exit(1)

    if password is None:
        logging.error("Error: FL_PASSWORD is not set.")
        sys.exit(1)

    session = authenticate(username, password)
    profile_ip = fetch_profile_ip(session)
    current_wan_ip = get_current_wan_ip()
    logging.info(f"Current WAN IP: {current_wan_ip}")
    logging.info(f"Profile Whitelist IP: {profile_ip}")

    # Initial check and update if necessary
    if current_wan_ip != profile_ip:
        logging.info("WAN IP does not match profile IP. Updating...")
        fetch_and_update_profile(session, current_wan_ip)
    else:
        logging.info("WAN IP matches profile IP. No update needed.")

    # Loop to check for IP changes
    while True:
        new_wan_ip = get_current_wan_ip()
        if new_wan_ip != current_wan_ip:
            logging.info(f"WAN IP changed to: {new_wan_ip}")
            current_wan_ip = new_wan_ip
            if not is_authenticated(session):
                logging.warning("Session expired, re-authenticating...")
                session = authenticate(username, password)
            fetch_and_update_profile(session, current_wan_ip)
        else:
            logging.info("No change in WAN IP.")

        # Wait for 1 minute before checking again
        sleep(60)
