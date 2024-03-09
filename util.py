# Utility functions
# Use one of these options in your file:
# Option 1 (preferred):
#   import util
#   util.function_name()
# Option 2:
#   from util import *
#   function_name()
import requests
import time

TBA_RETRY_COUNT = 10
KEY_PATH = 'var/tba-read-key.txt' # Path to your The Blue Alliance read API key
key = '' # The Blue Alliance read API key

def call_tba_api(url):
    """
    Call the TBA API with retries in case it is busy.

    Returns the response object so you can check for 200 or 404.
    Use .json() to get the data.
    """

    # Load the key from file if needed, prepare the request header
    global key
    if key == '':
        key = load_read_key()
    headers = {'X-TBA-Auth-Key': key}

    for i in range(TBA_RETRY_COUNT):
        try:
            return requests.get(url, headers=headers)
        except:
            print('TBA API busy, retrying...')
            time.sleep(1)
    print('TBA API busy, giving up...')
    exit()

def load_read_key(): 
    """Gets the API key from the first line of the file in var/tba-read-key.txt."""
    try:
        with open(KEY_PATH) as f:
            lines = f.readlines()
    except:
        print('Could not open ' + KEY_PATH)
        exit()
    
    if len(lines[0]) != 64:
        print('Invalid key, expected length of 64 characters')
        exit()
    return lines[0]