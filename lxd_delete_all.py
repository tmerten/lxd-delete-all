#!/usr/bin/env python3
""" This script deletes all LXC containers, profiles, networks and images.

This incldes running containers and OS images and
excludes default profiles.

The script assumes that the user running the script has non-sudo access
to lxc

No dependencies.

Author: Thorsten Merten
Author: Ilhaan Rasheed
"""

from typing import Any
import json
import subprocess
import argparse
import sys

app_description = """
This script can reset your entire LXD configuration to give you a fresh start.

You can also use it to delete particular parts (e.g. containers, 
images, networks, profiles) from LXD by using the corresponding switches.

The script is very destructive if you use the --delete-all flag. Please
consider excluding projects from resetting (using the -e switch).

For all the other flags, the script tries to delete what is specified
but does not force deletion.
"""

def get_args():
    """Get args from command line"""

    parser = argparse.ArgumentParser(
            description=app_description,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--delete-all', dest='reset',
                        default=False, action='store_true',
                        help='Enable this to delete everything in LXD.\n' \
                                'Exceptions are the default project and ' \
                                'default profiles')
    parser.add_argument('-c', '--containers', dest='container_delete',
                        default=False, action='store_true',
                        help='Enable this to delete all LXD containers')
    parser.add_argument('-i', '--images', dest='image_delete',
                        default=False,
                        action='store_true',
                        help='Enable this to delete all LXD images')
    parser.add_argument('-p', '--profiles', dest='profile_delete',
                        default=False,
                        action='store_true',
                        help='Enable this to delete all LXD profiles')
    parser.add_argument('-n', '--newworks', dest='network_delete',
                        default=False,
                        action='store_true',
                        help='Enable this to delete all LXD networks')
    parser.add_argument('-e', '--exclude-projects',
                        nargs="*", default=[], dest='exclude_projects',
                        help='Do not touch the following projects\n'\
                                f'E.g. {parser.prog} -e p1 proj2 --delete-all')
    args = parser.parse_args()

    if any(vars(args).values()):
        return args
    else:
        print("No arguments given. Use --help for more information.")
        sys.exit()

class LxdCleaner:
    """Encapsulates various LXD cleaning tasks and runs them for all
    projects."""
    def __init__(self, excluded_projects) -> None:
        self.projects:list[str] = []
        self._get_projects(excluded_projects)


    @staticmethod
    def _run_lxc_command(lxc_args:list[str], format_json:bool=False) -> Any:
        """Run a lxc command"""
        command = [ "lxc" ]
        if format_json:
            # unfortunately --format=json does not work for delete commands
            command.append("--format=json")
        command = command + lxc_args
   
        # run the lxc command and grab the output
        lxc_output = subprocess.run(
                command, stdout=subprocess.PIPE
                ).stdout.decode('utf-8')

        # Load json string output
        if format_json:
            return json.loads(lxc_output)
        else:
            return lxc_output


    def _get_projects(self, excluded_projects):
        data = self._run_lxc_command(["project", "list"], True)
        for project in data:
            if project not in excluded_projects:
                self.projects.append(project['name'])


    def reset(self):
        """Function that resets/deletes everything"""
        self.container_delete()
        self.image_delete()
        self.profile_delete()
        self.network_delete()


    def container_delete(self):
        """Function that deletes all containers"""

        for project in self.projects:
            # Run lxc list command to get JSON output as a string
            data = self._run_lxc_command([
                "list", "--project", project,
                 "--columns", "ns"
                ], True)

            # Create empty list to store LXC Container names
            containers = []
            for container in data:
                containers.append((container["name"], container["status"]))

            # Run LXD Delete command for each container
            for container in containers:
                if container[1] == 'Running':
                    # More gracefull, to stop first and delete afterwards
                    subprocess.run([
                        "/snap/bin/lxc",
                        "--project", project,
                        "stop", container[0]
                        ])
                subprocess.run([
                    "/snap/bin/lxc", "--project", project,
                     "delete", container[0]
                    ])


    def image_delete(self):
        """Function that deletes all images"""

        for project in self.projects:
            # Run lxc image list command to get JSON output as a string
            data = self._run_lxc_command([
                "image", "list", "--project", project
                ], True)

            # Create empty list to store LXC Image fingerprints
            image_fingerprints = []
            for image in data:
                image_fingerprints.append(image["fingerprint"])

            # Run LXD Image Delete command for each container
            for image in image_fingerprints:
                self._run_lxc_command([
                    "image", "--project", project, "delete", image
                    ])


    def profile_delete(self):
        """Function that deletes all profiles"""

        for project in self.projects:
            # Run lxc image list command to get JSON output as a string
            data = self._run_lxc_command([
                "profile", "list", "--project", project
                ], True)

            # Run LXD profile Delete command for each non-default profile
            for profile in data:
                if profile['name'] != 'default':
                    self._run_lxc_command([
                        "profile", "--project", project,
                        "delete", profile['name']
                        ])

    def network_delete(self):
        """Function that deletes all lxd managed networks"""

        for project in self.projects:
            # Run lxc image list command to get JSON output as a string
            data = self._run_lxc_command([
                "network", "list", "--project", project
                ], True)

            for network in data:
                if network['managed']:
                    self._run_lxc_command([
                        "network", "--project", project,
                        "delete", network['name']
                        ])

if __name__ == '__main__':
    args = get_args()
    lc = LxdCleaner(args.exclude_projects)
    
    if args.reset:
        lc.reset()
    else:
        if args.container_delete:
            lc.container_delete()
        if args.image_delete:
            lc.image_delete()
        if args.profile_delete:
            lc.profile_delete()
        if args.network_delete:
            lc.network_delete()
