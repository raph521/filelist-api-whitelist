#!/bin/bash

echo "The script will ask for your FileList credentials to pass them to the container. Be careful, the password will be visible while typing it."
echo ""

# Ask for username
read -p "Enter username: " username

# Create file "username" and insert the entered username
echo "$username" > username

# Ask for password
read -p "Enter password: " password

# Create file "password" and insert the entered password
echo "$password" > password

# Build Docker image with no cache
docker build --no-cache -t filelist-api-whitelist .

# Run Docker Compose up and detach
docker compose up --build -d

# Sleep for a moment to let Docker services start
sleep 5

# Remove temporary username and password files
rm username password

echo "Setup completed successfully, secrets have been deleted."
