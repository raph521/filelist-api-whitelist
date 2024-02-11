# filelist-api-whitelist

### Introduction

This is a simple python script which uses requests to update your whitelisted public IP in your FileList profile so that you can use *arr type aplications if your IP is dynamic.

Credentials must be specified via environment variables.

## Config

### Environment Variables

| Variable       | Example             | Default             | Description                  |
|----------------|---------------------|---------------------|------------------------------|
| `TZ`           | `America/New_York`  | `America/New_York`  | Timezone for use in logging  |
| `FL_USERNAME`  | `MyUser`            |                     | FileList username            |
| `FL_PASSWORD`  | `hunter2`           |                     | FileList password            |

## Docker Compose Example

```
version: '3.9'

services:
    filelist-api-whitelist:
        container_name: filelist-api-whitelist
        image: filelist-api-whitelist
        build:
            context: ./filelist-api-whitelist
            dockerfile: ./filelist-api-whitelist/Dockerfile
        environment:
            - TZ=${TZ}
            - FL_USERNAME=${FL_USERNAME}
            - FL_PASSWORD=${FL_PASSWORD}
```

### How to see container logs

```shell
docker logs -f filelist-api-whitelist
```

## Contributing
*Big thanks to Mnml*
Feel free to contribute or report bugs.
