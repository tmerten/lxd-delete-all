# lxd-delete-containers

**Important: This script can mess up your system and screw up everytying you did with LXD. Use at your own risk!**

The Python script in this repo can delete all [LXD](https://linuxcontainers.org/lxd/) profiles, containers, networks, and images on a machine. It is basically an extension of [Ilhaan Rasheed's Script to delete containers and images](https://github.com/ilhaan/lxd-delete-containers).

The main extension is, that everything can be deleted for all projects.

Resetting lxd entirely is the equivalent to running the following command for each container: 
```
lxc stop <container_name>  # for all running containers
lxc delete <container_name> 
lxc image delete <image_fingerprint>
lxc profile delete <profile_name>
lxc network delete <network_name> # for all lxd managed networks
```

This script has been tested on Ubuntu 22.10 with a `snap` installed LXD version of 5.7. 

## Requirements 

* Python3 
* Ability to run `lxc` without `sudo`

## Instructions

1. Clone this repo and `cd` into the cloned directory. 
2. Make sure you have execute permissions on `lxd_reset_all.py`. You can set this for the current user by running: `chmod u+x lxd_reset_all.py`
3. View available options: `./lxd_reset_all.py --help`
4. Reset everything: `./lxd_reset_all.py --reset-all`
   - Exclude a project: `./lxd_reset_all.py --reset-all -e my_project`
5. Delete containers: `./lxd_reset_all.py -c`
6. Delete images: `./lxd_reset_all.py -i`
7. Delete profiles: `./lxd_reset_all.py -p`
8. Delete networks: `./lxd_reset_all.py -n`

Alternatively, you can run this script without cloning the repo using [`curl`](https://curl.haxx.se/). For example, the following command runs the script and displays it's help message: 
```
curl -s https://raw.githubusercontent.com/tmerten/lxd-delete-all/master/lxd_delete_all.py | python3 - -h 
```
