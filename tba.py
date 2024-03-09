import datetime
import util

# Your event and team
EVENT_KEY = '2023wimi'
TEAM = 'frc6223'

# URL to get the match detail from TBA API
URL_START = 'https://www.thebluealliance.com/api/v3/team/'
URL_MID = '/event/'
URL_END = '/matches/simple'

# This is used to test on a previous event
FAKE_DATE = '2023-03-24 12:00'

# How many matches to output
MATCH_COUNT = 5

# Build the URL, call the Blue Alliance API, return a parsed JSON array
def get_team_matches():
    url = URL_START + TEAM + URL_MID + EVENT_KEY + URL_END 
    return util.call_tba_api(url).json()
        
# The core program!!
def main():
    matches = get_team_matches()

    # Use either now or the fake target and comment out the other line
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