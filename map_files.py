import os
import argparse

"""Parsing program arguments"""
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--rootdir',
                    help="from which directory to print the files.",
                    required=True, metavar='')
options = parser.parse_args()


def map_files(root_dir=os.getcwd()):
    """Print all files and directories from given root directory.
    
    Args:
        root_dir - string: path to the wanted directory in the agent machine.
    
    Raises:
        ValueError: an Error occurred accessing the given directory's path.
    """
    if not os.path.exists(root_dir):
        raise ValueError
    
    queue = [root_dir]
    
    while queue:
        # Pop out directory name from queue
        curr_dir = queue.pop(0)
        # Initalize list for the files
        files = []
        # Set the current directory we search in
        curr_dir = os.path.join(root_dir, curr_dir)
        
        # Iterate over the content of the current directory
        # Determine which one is a file and which one is a directory
        # Update the directories queue and the file list.
        for f in os.listdir(curr_dir):
            path = os.path.join(curr_dir, f)
            if os.path.isdir(path):
                queue.append(path)
            elif os.path.isfile(path):
                files.append(path)
                
        print("[DIR] " + curr_dir)
        for f in files:
            print("\t[FILE] " + f)
    
    
if __name__ == '__main__':
    root_dir = options.rootdir
    try:
        map_files(root_dir)
    except ValueError:
        print("No such file or directory such as " + root_dir)
