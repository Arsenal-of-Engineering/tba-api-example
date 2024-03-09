import requests
import json
import datetime
import time
import util

# Path to your The Blue Alliance read API key
KEY_PATH = 'var/tba-read-key.txt'

# Default event and team
EVENT_KEY = '2024mndu'
TEAM = 'frc1732'

# URL to get the match detail from TBA API
URL_START = 'https://www.thebluealliance.com/api/v3/team/'
URL_MID = '/event/'
URL_END = '/matches?X-TBA-Auth-Key='
URL_EVENT_START = 'https://www.thebluealliance.com/api/v3/event/'


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
def get_team_matches(team, event):
    url = URL_START + team + URL_MID + event + URL_END
    return util.call_tba_api(url)
    
   
# The core program!!
def main():

    keep_asking = True
    while(keep_asking):
        input_team = input("Enter team [press enter for default of 1732]: ")

        if input_team:
            team = 'frc' + input_team

            url = URL_START + team
            if util.call_tba_api(url).status_code == 404:
                print('Team ' + input_team + ' is not a valid team. Please try again.')
            else:
                keep_asking = False
        else:
            team = TEAM
            keep_asking = False

    
    keep_asking = True
    while(keep_asking):
        input_event = input("Enter an event code [press enter for default of 2024mndu]: ")

        if input_event:
            event = input_event

            url = URL_EVENT_START + event
            if util.call_tba_api(url).status_code == 404:
                print('Event ' + event + ' is not a valid event. Please try again.')
            else:
                keep_asking = False
        else:
            event = EVENT_KEY
            keep_asking = False


    matches = get_team_matches(team, event).json()
    if len(matches) != 0:
        # Variables we use to sum up the metrics
        vals = []
        percents = {'autoLeaveCount':0, 'parkCount':0, 'hangCount':0, 'wins':0}
        scores = {
            'autoAmpNoteCount':0, 
            'autoSpeakerNoteCount':0, 
            'teleopAmpNoteCount':0, 
            'teleopSpeakerNoteCount':0, 
            'teleopSpeakerNoteAmplifiedCount':0, 
            'autoPoints':0, 
            'teleopTotalNotePoints':0, 
            'endGameTotalStagePoints':0, 
            'foulPoints':0, 
            'totalPoints':0, 
            'rp':0}
        match_count = 0

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
                for key in scores:
                    scores[key] += m['score_breakdown'][color][key]

                if m['winning_alliance'] == color:
                    percents['wins'] = percents.get('wins', 0) + 1

        print('-----------------------------------')
        print(' Team:', team, ' at event:', event)
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
    else:
        print('Team: ' + team + ' was not at event ' + event + ' or it hasn''t happened yet.')


# This is a standard python convention to trigger the call to the main function
if __name__ == '__main__':
    main()