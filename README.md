# YouTube Automation
Using YouTube's API, this repository will work toward automating tedious tasks for YouTube channels. **The main objective is to update YouTube Descriptions with the number of likes, dislikes, likes/(likes+dislikes), timestamp** up to the YouTube API limit. Check out my [YouTube Like, Dislike Counter Playlist](https://youtube.com/playlist?list=PLHT3ZrWZ1pcSFjYuMPwa0m0pjB4fUP5c_)!

# Requirements:
- Python >= 3.7
````
pip install -r requirements.txt
````

# Setup Requirements
- Need YouTube account
- Create **.env** file in root directory
````
# Contents of .env
CLIENT_SECRET_FILE=client_secret_web_app.json
CHANNEL_ID='YOUR_CHANNEL_ID'
````
- Need to enable API (YouTube Data API V3)
- **You have the choice to choose which OAuth to use; In production, I used Web App**
  - Need to create OAuth Client ID: > Web App > Name Web App App > Create > Download OAuth Client (JSON)
    - This will be your web app secret file. **(Renamed downloaded OAuth Client to client_secret_web_app.json)**
- Setup up OAuth Consent Screen
  - Make sure to add your testing email as a test user to access your YouTube account (need to manually do this)
-   Ensure to verify your application! Run the following:
  ````
  # creates a token.pickle file   
  from ytad.authentication import Authenticate
  auth = Authenticate()
  youtube = auth.check_token_web_app_data_api()
  ````
# Example: [Command Line Interface (CLI) explained](https://youtu.be/yrzP762gV1I)
````
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
- setup.py (on pypi) for installation

# Remaining TODOs:
- [ ] Verify setup with @SpencerPao
- [ ] Overhaul CLI (maybe this should be another issue and version though)
- [ ] Test API and authentication
- [ ] Create PyPI and TestPyPI accounts
- [ ] Build package wheel
- [ ] Test package with `twine`
- [ ] Upload package with `twine`
- [ ] Try installing with `pip`
