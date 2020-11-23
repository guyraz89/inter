import os
import argparse
from paramiko import SSHClient
from paramiko.ssh_exception import SSHException, NoValidConnectionsError
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
    except SSHException:
        print("[ERROR] command execution failed.")
        for line in ssh_stderr.read().readlines():
            print(line)
    except NoValidConnectionsError:
        print("[ERROR] Failed to establish connection")
        for line in ssh_stderr.read().readlines():
            print(line)
    except IOError:
        print("[ERROR] Upload script to remote machine has failed\n check your input arguments")

    finally:
        ssh.close()