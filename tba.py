import requests
import json
import datetime
import time

# Path to your The Blue Alliance read API key
KEY_PATH = 'var/tba-read-key.txt'

# Your event and team
EVENT_KEY = '2023wimi'
TEAM = 'frc6223'

# URL to get the match detail from TBA API
URL_START = 'https://www.thebluealliance.com/api/v3/team/'
URL_MID = '/event/'
URL_END = '/matches/simple?X-TBA-Auth-Key='

# This is used to test on a previous event
FAKE_DATE = '2023-03-24 15:00'

# How many matches to output
MATCH_COUNT = 3


# Gets the key from the first line of the file in var/tba-read-key.txt
def load_read_key(): 
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

# Build the URL, call the Blue Alliance API, return a parsed JSON array
def get_team_matches(key):
    url = URL_START + TEAM + URL_MID + EVENT_KEY + URL_END + key
    return requests.get(url).json()
        
# The core program!!
def main():
    tba_read_key = load_read_key()
    matches = get_team_matches(tba_read_key)

    # Use either now or the fake target and commentt out the other line
    #date_target = datetime.datetime.now()
    date_target = datetime.datetime.strptime(FAKE_DATE,"%Y-%m-%d %H:%M")

    # Convert the target date into UNIX format
    unix_target = datetime.datetime.timestamp(date_target)

    # Loop through the matches and print the next 3
    matches_printed = 0
    for m in matches:
        # Assuming predicted_time is what we need
        timestamp = datetime.datetime.fromtimestamp(m['predicted_time'])

        if timestamp > date_target:
            # Make a human-readable version for later use
            match_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

            # Get the blue teams in a string, stripping off the 'frc' prefix
            blue = ' BLUE:'
            for t in m['alliances']['blue']['team_keys']:
                blue += t.replace('frc', ' ')

            # Same for red
            red = '  RED:'
            for t in m['alliances']['red']['team_keys']:
                red += t.replace('frc', ' ')

            # Print our color first
            if TEAM.replace('frc', '') in blue:
                print(match_time + blue + red)
            else:
                print(match_time + red + blue)
           
            # Only output the specified amount of upcoming matches
            matches_printed += 1
            if matches_printed >= MATCH_COUNT:
                break

# This is a standard python convention to trigger the call to the main function
if __name__ == '__main__':
    main()