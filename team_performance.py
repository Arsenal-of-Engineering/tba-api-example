import requests
import json
import datetime
import time

# Path to your The Blue Alliance read API key
KEY_PATH = 'var/tba-read-key.txt'

# Your event and team
EVENT_KEY = '2024mndu'
TEAM = 'frc1732'
# TEAM = 'frc6160'

# URL to get the match detail from TBA API
URL_START = 'https://www.thebluealliance.com/api/v3/team/'
URL_MID = '/event/'
URL_END = '/matches?X-TBA-Auth-Key='

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
def get_team_matches(key, team):
    url = URL_START + team + URL_MID + EVENT_KEY + URL_END + key
    return requests.get(url).json()

# The core program!!
def main():
    input_team = input("Enter team [press enter is default]: ")
    if input_team:
        team = 'frc' + input_team
    else:
        team = TEAM

    tba_read_key = load_read_key()
    matches = get_team_matches(tba_read_key, team)
    # print(matches)

    vals = []
    percents = {}
    scores = {}
    match_count = 0

    percents = {'autoLeaveCount':0, 'parkCount':0, 'hangCount':0, 'wins':0}

    score_keys = ['autoAmpNoteCount', 'autoSpeakerNoteCount', 'teleopAmpNoteCount', 'teleopSpeakerNoteCount', 'teleopSpeakerNoteAmplifiedCount', 'autoPoints', 'teleopTotalNotePoints', 'endGameTotalStagePoints', 'foulPoints', 'totalPoints', 'rp']
    # for key in score_keys:
    #     scores[key] = 0


    for m in matches:
        # Ignore matches that have not been played yet or finals skipped
        if m['actual_time'] is not None:
            match_count += 1

            match = m['comp_level'] + str(m['match_number'])
            color = ''
            team_pos = 0

            # Figure out color and position
            for i, t in enumerate(m['alliances']['blue']['team_keys']):
                if t == team:
                    color = 'blue'
                    team_pos = i + 1
                    break
            for i, t in enumerate(m['alliances']['red']['team_keys']):
                if t == team:
                    color = 'red'
                    team_pos = i + 1
                    break

            # Get percentage metrics
            key = 'autoLineRobot' + str(team_pos)
            if m['score_breakdown'][color][key] == 'Yes':
                percents['autoLeaveCount'] = percents.get('autoLeaveCount', 0) + 1

            key = 'endGameRobot' + str(team_pos)
            leave = m['score_breakdown'][color][key]
            if leave == 'Parked':
                percents['parkCount'] = percents.get('parkCount', 0) + 1
            elif  'Stage' in leave:
                percents['hangCount'] = percents.get('hangCount', 0) + 1

            # Get score metrics
            for key in score_keys:
                scores[key] = scores.get(key, 0) + m['score_breakdown'][color][key]

            # print('did', color, 'win? ', m['winning_alliance'] )
            if m['winning_alliance'] == color:
                percents['wins'] = percents.get('wins', 0) + 1

    print('-----------------------------------')
    print(' Team:', team, ' at event:', EVENT_KEY)
    print('-----------------------------------')
    print('Robot specific metrics:')

    # Print percentage metrics
    for key in percents.keys():
        val = str(round(percents[key]/match_count*100, 1)) + '%'
        print(val.rjust(6, ' '), ':', key)
    print()

    print('Alliance average metrics:')
    # Print score metrics
    for key in scores.keys():
        if key == 'autoPoints':
            print()
        val = str(round(scores[key]/match_count, 1))
        print(val.rjust(6, ' ') , ':', key )


# This is a standard python convention to trigger the call to the main function
if __name__ == '__main__':
    main()