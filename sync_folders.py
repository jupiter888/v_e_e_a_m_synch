import os
import sys
import time


def synchronize_folders(source_folder, replica_folder, log_file):
    # verify replica folder exists
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # log file operations to the console & log file
    def log_operation(operation, path):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f'[{timestamp}] {operation}: {path}'
        print(message)
        log_file.write(f'{message}\n')

    # synchronize files & directories
    def sync_files(source, replica):
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            replica_path = os.path.join(replica, item)

            if os.path.isfile(source_path):
                if os.path.exists(replica_path):
                    if os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                        log_operation('Updating', replica_path)
                        shutil.copy2(source_path, replica_path)
                else:
                    log_operation('Copying', replica_path)
                    shutil.copy2(source_path, replica_path)
            elif os.path.isdir(source_path):
                if not os.path.exists(replica_path):
                    os.makedirs(replica_path)
                sync_files(source_path, replica_path)

    # perform initial synchronization
    sync_files(source_folder, replica_folder)

    # synchronize periodically
    while True:
        time.sleep(interval)
        sync_files(source_folder, replica_folder)


if __name__ == '__main__':
    import argparse
    import shutil

    # create argument parser
    parser = argparse.ArgumentParser(description='Folder synchronization script')

    # add cmd line args
    parser.add_argument('source', help='Path to the source folder')
    parser.add_argument('replica', help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', help='Path to the log file')

    # parse cmd line arguments
    args = parser.parse_args()

    # open the log file
    with open(args.log_file, 'a') as log:
        # call the synchronize_folders function
        synchronize_folders(args.source, args.replica, log)

# Run the following command in the terminal 
# python sync_folders.py /path/to/source /path/to/replica 60 /path/to/log.txt
