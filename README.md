# tba-api-example
Example of how to use The Blue Alliance API to get match information.

`tba.py`: It returns a list of upcoming matches for a specified team and event greater than the specified timestamp.

`team_performance.py`: For a given event, summarizes average game performance for a team.

'MatchMetrics.ipynb': A data analysis "notebook" that displays several charts and statistics.

## How to run
1. Clone this repository: [general instructions here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
2. Install the package to call APIs called `requests`.  Either install it globally or create a virtual environment (preferred).  
    Here is how to do it with a virtual environment in WSL (linux on windows - the $ is your prompt, commands vary in Windows):
    ```
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install requests
    ```
    Remember that you will need to activate your virtual environment on your next session with `source .venv/bin/activate`
3. Go to The [Blue Alliance Account](https://www.thebluealliance.com/account) page and create a new Read API Key.
4. Create a new directory and file: `var/tba-read-key.txt` and paste your key there.  This directory is excluded via `.gitignore` so it would not be in the public repository.
5. Run from a command-line:

    **Upcoming matches:**

    `(.venv) $ python tba.py`

    Given a target date of 2023-03-24 15:00 for team 6223 at the Milwaukee regional, output should be:
    ```
    2023-03-24 15:36:37 BLUE: 5822 6223 8701  RED: 6574 7900 7915
    2023-03-24 16:42:14 BLUE: 6223 7417 7915  RED: 706 8188 2077
    2023-03-24 17:32:51  RED: 4787 2506 6223 BLUE: 5148 6421 8096
    ```

    **Team performance at a match:**

    `(.venv) $ python team_performance.py`
    ```
    Enter team [press enter for default]: 930
    -----------------------------------
     Team: frc930  at event: 2024mndu
    -----------------------------------
    Robot specific metrics:
     91.7% : autoLeaveCount
     91.7% : parkCount
      0.0% : hangCount
     58.3% : wins

    Alliance average metrics:
      0.0 : autoAmpNoteCount
      2.3 : autoSpeakerNoteCount
      3.2 : teleopAmpNoteCount
      6.6 : teleopSpeakerNoteCount
      1.7 : teleopSpeakerNoteAmplifiedCount

     16.8 : autoPoints
     24.7 : teleopTotalNotePoints
      4.5 : endGameTotalStagePoints
      3.9 : foulPoints
     49.9 : totalPoints
      1.6 : rp
    ```

6. When you are done, deactivate the virtual environment with `deactivate`

## Development notes
* The TBA API uses unix timestamps.  So, you will see some code that converts unix to/from a date object, and then other code to convert date objects to/from a human-readable string.
* The API returns JSON and this is easily converted into Python arrays and dictionaries.
* All constants are at the top of the file