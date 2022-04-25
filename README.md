# YouTube Automation
Using YouTube's API, this repository will work toward automating tedious tasks for YouTube channels. **The main objective is to update YouTube Descriptions with the number of likes, dislikes, likes/(likes+dislikes), timestamp** up to the YouTube API limit. Check out my [YouTube Like, Dislike Counter Playlist](https://www.youtube.com/watch?v=g9x_Eg5G-LI&list=PLHT3ZrWZ1pcSFjYuMPwa0m0pjB4fUP5c_&index=1)!

# Requirements:
- Python >= 3.7
- [PyPi distribution](https://pypi.org/project/ytad/)
````
pip install ytad
````

# Setup Requirements
- Need YouTube account with at least one public video
- Register your account with [Google console developers](https://console.developers.google.com)
- Need to enable API (YouTube Data API V3)

- **You have the choice to choose which OAuth to use; In production, I used Web App**
  - Create OAuth Client ID: > Web App > Name Web App App > Create > Download OAuth Client (JSON)
    - This will be your web app secret file. **(Rename downloaded OAuth Client to client_secret_web_app.json)**
- Setup up OAuth Consent Screen
  - Make sure to add your testing email as a test user to access your YouTube account (need to manually do this)
-   Ensure to verify your application! Run the following:
  ````
  # creates a token.pickle file for authentication
  from ytad.authentication import Authenticate
  auth = Authenticate()
  youtube = auth.check_token_web_app_data_api()
  ````
# Command Line Interface (CLI) capability:
- In base environment, you need the following files to run: **U**pdate **V**ideo **D**escription (**uvd**) successfully:
  - client_secret_web_app.json
  - token.pickle
````
uvd -h # input your arguments for ease of use.
# example (Using my YouTube Channel ID as an example...)
uvd --id=UCoCToADdJRd3u-ACz4e_iCw
````
# [Deprecated] [Command Line Interface (CLI) explained](https://youtu.be/yrzP762gV1I)
````
"""This has been deprecated; see above for more integrated CLI capabilities"""
python update_notifications.py --help
python .\update_notifications.py --update_df=Yes --verify_each_update=Yes
````

# Cloud
I used AWS services to ensure a cron job (in production) is enacted. This is a low cost solution, utlizing lambda functions and minimial time on Ec2 instances.
- The cloud setup and infrastructure can be found [here](https://youtu.be/Q3mIrtMw_3E)

# Goals of Library:
- <strike> Scrape personal Likes/Dislikes from backend (YouTube Studio) </strike>
- <strike> Automating the update(s) of descriptions in videos </strike>
- <strike> Executable with parameters and pip installable </strike>
- <strike> cron job </strike>
- <strike> Minimization of YouTube Requests </strike>
- <strike> Keygen for API calls </strike>
- <strike> argparse: CLI enabled. </strike>
- <strike> setup.py (on pypi) for installation </strike>

# Remaining TODOs:
- [x] Verify setup with @SpencerPao
- [x] Overhaul CLI (maybe this should be another issue and version though)
- [x] Test API and authentication
- [x] Create PyPI and TestPyPI accounts
- [x] Build package wheel
- [x] Test package with `twine`
- [x] Upload package with `twine`
- [x] Try installing with `pip`
