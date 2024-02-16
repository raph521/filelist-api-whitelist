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
        image: ghcr.io/raph521/filelist-api-whitelist:nightly
        environment:
            - TZ=${TZ}
            - FL_USERNAME=${FL_USERNAME}
            - FL_PASSWORD=${FL_PASSWORD}
```

## Container Logs

```shell
docker logs -f filelist-api-whitelist
```

## Contributing
*Big thanks to Mnml*

Feel free to contribute or report bugs.
