# filelist-api

### Introduction

This is a simple python script which uses requests to update your whitelisted public IP in your FileList profile so that you can use *arr type aplications if your IP is dynamic.

### How to build

```shell
docker build -t filelist-api-whitelist .
```

## How to run

### docker-compose.yml

1. Create secrets:

``` shell
echo "myUsername" | docker secret create my_username -
echo "myPassword" | docker secret create my_password -
```

2. docker-compose.yml

```
version: '3.2'
services:
    changedetection:
      image: myregistry.example.com/filelist-api-whitelist:1 .
      container_name: filelist-api-whitelist
      environment:
        - FL_USERNAME=/run/secrets/my_username
        - FL_PASSWORD=/run/secrets/my_password
      restart: unless-stopped
```

### Quick and dirty (NOT RECOMMENDED)

There is a reson why have to do this so plese don't keep username/passwords in plain text.

But if you know what you are doing... here you go.

Compose file
```
version: '3.2'
services:
    changedetection:
      image: myregistry.example.com/filelist-api-whitelist:1 .
      container_name: filelist-api-whitelist
      environment:
        - FL_USERNAME=YOUR_USER
        - FL_PASSWORD=YOUR_PASSWORD
      restart: unless-stopped
```

## Contributing

Feel free to contribute or report bugs.
