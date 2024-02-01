# filelist-api

### Introduction

This is a simple python script which uses requests to update your whitelisted public IP in your FileList profile so that you can use *arr type aplications if your IP is dynamic.

Keep in mind that you cannot restart the container, you need to rebuild it with setup.sh because the credentials are not persistent for security reasons. See last section.

### How to build and run
Make sure you have docker installed and that your current user can issue docker commands.  
https://docs.docker.com/engine/install/linux-postinstall/

```shell
mkdir ~/your_preferred_folder/
cd ~/your_preferred_folder/
git clone https://github.com/DevilRange/filelist-api-whitelist/
cd ~/your_preferred_folder/filelist-api-whitelist/
chmod u+x setup.sh
./setup.sh
```

### How to see container logs

```shell
docker logs -f filelist-api
```

### How to fix if you mistype your credentials or if you need to restart

```shell
docker rm -f filelist-api
docker prune -a
cd ~/your_preferred_folder/filelist-api-whitelist/
./setup.sh
```

## Contributing
*Big thanks to Mnml*  
Feel free to contribute or report bugs.
