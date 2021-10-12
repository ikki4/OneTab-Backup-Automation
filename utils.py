import os
import shutil
from pathlib import Path


def create_directory_if_not_exists(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


def remove_directory_if_exists(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath)


def copy_directory(src, dest):
    shutil.copytree(src, dest)


def remove_all_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                remove_directory_if_exists(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def copy_all_files_in_directory(directory_path, destination_path, exception_file_name=[]):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if filename in exception_file_name:
            continue

        shutil.copy(file_path, destination_path)

        
def remove_oldest_files_in_directory(directory_path, files_to_keep=30): #new
    '''Keeps in the folder only the 30 most recent* text files (the number can be changed).
    *The most recent files are the ones with the latest "last modification" date.'''
    p=Path(directory_path)
    total_files = len(sorted(p.glob("*.txt"), key=os.path.getmtime))
    if  total_files > files_to_keep:
        diff = total_files - files_to_keep
        for file in sorted(p.glob("*.txt"), key=os.path.getmtime)[:diff]:
            try:
                os.unlink(file)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file, e))
