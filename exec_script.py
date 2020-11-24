import os
import sys
import argparse
from paramiko import SSHClient
from paramiko.ssh_exception import SSHException, AuthenticationException, BadHostKeyException
from paramiko.client import AutoAddPolicy

"""Parsing program arguments"""
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--rootdir',
                    help="from which directory to print the files.",
                    required=True, metavar='')
parser.add_argument('-n', '--hostname',
                    help="remote machine address.",
                    required=True, metavar='')
parser.add_argument('-u', '--username',
                    help="user name of the remote machine.",
                    required=True, metavar='')
parser.add_argument('-p', '--password',
                    help="password of the remote machine.",
                    required=True, metavar='')
parser.add_argument('-o', '--port',
                    help="port.",
                    required=True, metavar='')
parser.add_argument('-s', '--script_name',
                    help="name of the script we want to launch on the remote machine.",
                    required=True, metavar='')

options = parser.parse_args()


if __name__ == '__main__':
    root_dir = options.rootdir
    hostname = options.hostname
    script_name = options.script_name
    port = options.port
    username = options.username
    password = options.password
    rc = 0
    try:
        # Connect remote machine via SSH
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password, port=port)
        # transfer file to wanted location on remote machine
        sftp = ssh.open_sftp()
        sftp.put(script_name, f'{root_dir}/{script_name}')
        sftp.close()
        # Run the script
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"python3 {root_dir}/{script_name}")
        # Read stdout
        for line in ssh_stdout.read().splitlines():
            print(line.decode())

    except ValueError:
        rc = 1
        print("[ERROR] No such file or directory such as " + root_dir)
    except BadHostKeyException:
        rc = 2
        print("[ERROR] Host key could not verified.")
    except AuthenticationException:
        rc = 3
        print("[ERROR] Authentication Failed")
    except SSHException:
        rc = 4
        print("[ERROR] Failed to establish connection.")
    except IOError:
        rc = 5
        print("[ERROR] Transfer script to remote machine has failed\n check your input arguments")

    finally:
        ssh.close()
        sys.exit(rc)
