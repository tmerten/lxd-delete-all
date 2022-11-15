# lxd-delete-all.py

**Important: This script can mess up your system and screw up everytying you did with LXD. Use at your own risk!**

## About

The Python script in this repo can delete all [LXD](https://linuxcontainers.org/lxd/) profiles, containers, networks, and images on a machine. It is basically an extension of [Ilhaan Rasheed's Script to delete containers and images](https://github.com/ilhaan/lxd-delete-containers). And this extension basically is, that everything can be deleted for all projects.

Resetting lxd entirely (e.g. using `--delete-all` is the equivalent to running the following command for each container for each project: 
```
lxc --project=<project_name> stop <container_name>  # for all running containers
lxc --project=<project_name> delete <container_name> 
lxc --project=<project_name> image delete <image_fingerprint>
lxc --project=<project_name> profile delete <profile_name>
lxc --project=<project_name> network delete <network_name> # for all lxd managed networks
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
5. Delete containers: `./lxd_reset_all.py -c`
6. Delete images: `./lxd_reset_all.py -i`
7. Delete profiles: `./lxd_reset_all.py -p`
8. Delete networks: `./lxd_reset_all.py -n`
9. Exclude a project: `./lxd_reset_all.py --reset-all -e myproject`
   - Exclude more projects: `./lxd_reset_all.py -c -e myproject1 myproject2`

Alternatively, you can run this script without cloning the repo using [`curl`](https://curl.haxx.se/). For example, the following command runs the script and displays it's help message: 
```
curl -s https://raw.githubusercontent.com/tmerten/lxd-delete-all/master/lxd_delete_all.py | python3 - -h 
```
