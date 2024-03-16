import datetime
import util

# Your event and team
EVENT_KEY = '2024wimi'
TEAM = 'frc6223'

# URL to get the match detail from TBA API
URL_START = 'https://www.thebluealliance.com/api/v3/team/'
URL_MID = '/event/'
URL_END = '/matches/simple'

# This is used to test on a previous event
FAKE_DATE = '2023-03-24 12:00'

# How many matches to output
MATCH_COUNT = 3

# Build the URL, call the Blue Alliance API, return a parsed JSON array
def get_team_matches():
    url = URL_START + TEAM + URL_MID + EVENT_KEY + URL_END 
    # print(url)
    return util.call_tba_api(url).json()
        
# The core program!!
def main():
    matches = get_team_matches()

    # Use either now or the fake target and comment out the other line
    date_target = datetime.datetime.now()
    # date_target = datetime.datetime.strptime(FAKE_DATE,"%Y-%m-%d %H:%M")

    future_matches = []

    # Loop through the matches and store future ones (they are not in sort order)
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

            match_num = ' Match: ' + str(m['match_number'])

            # Print our color first
            if TEAM.replace('frc', '') in blue:
                future_matches .append(match_time + blue + red + match_num)
            else:
                future_matches .append(match_time + red + blue + match_num)

    future_matches.sort()

    for i in range(MATCH_COUNT):
        print(future_matches[i])    
        teams = future_matches[i].split()
        for j in (3, 4, 5, 7, 8, 9):
            url = f"https://www.thebluealliance.com/api/v3/team/frc{teams[j]}/event/{EVENT_KEY}/status"
            data = util.call_tba_api(url).json()
            wlt = str(data['qual']['ranking']['record']['wins']) + '-' + str(data['qual']['ranking']['record']['losses']) + '-' + str(data['qual']['ranking']['record']['ties'])
            mp = '(' + str(data['qual']['ranking']['matches_played']) + ')'
            print('  ', teams[j],  data['qual']['ranking']['rank'], wlt, mp)


# This is a standard python convention to trigger the call to the main function
if __name__ == '__main__':
    main()