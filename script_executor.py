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
parser.add_argument('-s', '--script_path',
                    help="from which directory to print the files.",
                    required=True, metavar='')

options = parser.parse_args()


if __name__ == '__main__':
    root_dir = options.rootdir
    hostname = options.hostname
    script_path = options.script_path
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
        sftp.put(script_path, f'{root_dir}/list_files.py')
        sftp.close()
        # Run the script
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"python3 {root_dir}/list_files.py")
        # Read stdout
        for line in ssh_stdout.read().splitlines():
            print(line.decode())

    except ValueError:
        print("[ERROR] No such file or directory such as " + root_dir)
        rc = 1
    except BadHostKeyException:
        rc = 3
        print("[ERROR] Host key could not verified.")
    except AuthenticationException:
        rc = 4
        print("[ERROR] Authentication Failed")
        for line in ssh_stderr.read().readlines():
            print(line)
    except SSHException:
        print("[ERROR] Failed to establish connection.")
        rc = 2
        for line in ssh_stderr.read().readlines():
            print(line)
    except IOError:
        rc = 5
        print("[ERROR] Transfer script to remote machine has failed\n check your input arguments")

    finally:
        ssh.close()
        sys.exit(rc)