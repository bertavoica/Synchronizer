import sys
import logging
import threading
import os
from dirsync import sync

SOURCE_FOLDER = ''
DESTINATION_FOLDER = ''
LOG_FOLDER = ''
SYNC_INTERVAL_SECONDS = 0


def check_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def configure_logger():
    """
    Configures internal logger to output the messages to the console and to the file (bullet 3)
    """
    # noinspection PyArgumentList
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(LOG_FOLDER, 'debug.log')),
            logging.StreamHandler(sys.stdout)
        ]
    )


def synchronize_folders():
    """"
    Synchronizes folders and logs the result from the sync action (bullet 1 and 2)
    """
    logging.info('Starting synchronizing folders between ' + SOURCE_FOLDER + ' and ' + DESTINATION_FOLDER)
    threading.Timer(SYNC_INTERVAL_SECONDS, synchronize_folders).start()
    sync(SOURCE_FOLDER, DESTINATION_FOLDER, 'sync', purge=True, verbose=True)


def is_valid_input(input_folder):
    """"
    Checks if the given directories are valid (exists and are folders)
    """
    return os.path.exists(input_folder) and os.path.isdir(input_folder)


def print_usage():
    print('Usage: synchronize.py source_folder destination_folder log_folder synchronization_interval \n'
          'source_folder,               original folder that is monitored for syncing\n'
          'destination_folder,          replica of the original folder in which we are going to copy content,\n'
          'log_folder,                  folder that contains debug.log,\n'
          'synchronization_interval,    interval between synchronizations')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage()
        sys.exit()

    # Extract information from the command line (bullet 4)
    SOURCE_FOLDER = sys.argv[1]
    DESTINATION_FOLDER = sys.argv[2]
    LOG_FOLDER = sys.argv[3]

    configure_logger()
    if not check_int(SYNC_INTERVAL_SECONDS):
        logging.error('Sync interval value is not integer')
        sys.exit()

    SYNC_INTERVAL_SECONDS = int(sys.argv[4])

    if not is_valid_input(SOURCE_FOLDER):
        logging.error('Source folder is not valid')
        sys.exit()

    if not is_valid_input(DESTINATION_FOLDER):
        logging.error('Destination folder is not valid')
        sys.exit()

    if not is_valid_input(LOG_FOLDER):
        logging.error('Log folder is not valid')
        sys.exit()

    synchronize_folders()
