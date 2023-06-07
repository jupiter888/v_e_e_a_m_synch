import argparse
import os
import shutil
import time
from datetime import datetime

def synchronize_folders(source_folder, replica_folder, interval, log_file):
    # create or clear the log file
    with open(log_file, 'w') as file:
        file.write('Synchronization Log\n\n')

    while True:
        start_time = time.time()

        # perform synchronization
        synchronize(source_folder, replica_folder, log_file)

        end_time = time.time()

        # calculate remaining time until the next synchronization
        elapsed_time = end_time - start_time
        remaining_time = interval - elapsed_time

        if remaining_time > 0:
            # wait for the remaining time before next synchronization
            time.sleep(remaining_time)

def synchronize(source_folder, replica_folder, log_file):
    # retrieve the existing files in the replica folder
    replica_files = set()
    for root, _, files in os.walk(replica_folder):
        for file in files:
            replica_files.add(os.path.join(root, file))

    # perform one-way synchronization from source to replica
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica_folder, os.path.relpath(source_path, source_folder))

            if replica_path not in replica_files or os.path.getmtime(source_path) > os.path.getmtime(replica_path):
                # file does not exist in replica or is newer in source, so copy it
                shutil.copy2(source_path, replica_path)
                log_operation('Copied', source_path, replica_path, log_file)

                # add the replica file to the set
                replica_files.add(replica_path)

    # remove files from replica that no longer exist in source
    for replica_file in replica_files:
        source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))

        if not os.path.exists(source_file):
            # file does not exist in source, so remove it from replica
            os.remove(replica_file)
            log_operation('Removed', replica_file, None, log_file)

            # remove the replica file from the set
            replica_files.remove(replica_file)

def log_operation(operation, source_path, replica_path, log_file):
    # log the file operation to both console and log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f'{timestamp} - {operation}: {source_path}'
    if replica_path:
        log_entry += f' -> {replica_path}'

    print(log_entry)
    with open(log_file, 'a') as file:
        file.write(log_entry + '\n')

def get_backup_info(replica_folder, log_file):
    # retrieve the latest backup timestamp and operation from the log file
    latest_backup_timestamp = None
    latest_backup_operation = None

    with open(log_file, 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if line.startswith('20'):
                timestamp = line.split(' - ')[0]
                operation = line.split(':')[0].split(' ')[-1]

                latest_backup_timestamp = timestamp
                latest_backup_operation = operation

                break

    # count the number of backup operations in the log file
    backup_count = 0
    with open(log_file, 'r') as file:
        for line in file
