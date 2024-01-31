FROM python:alpine

WORKDIR /usr/src/app

RUN apk add --no-cache bash

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x filelist_whitelist_ip.py

CMD ["python", "filelist_whitelist_ip.py"]
