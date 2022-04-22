#!/bin/env python
"""Make sure to check out
https://github.com/mCodingLLC/mCodingYouTube/tree/master/mcoding_youtube Lots
of setup inspiration came from his code!

Wrapper around Google's OAuth2 authentication process providing
convenience functions to build service objects.
"""

from typing import Iterator
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

# Google's Request
from google.auth.transport.requests import Request


class Authenticate:
    def __init__(self):
        pass

    def check_token_web_app_data_api(self):
        """Used for client_secret_web_app (Webapp keys from Google OAUTH)
        Source: Corey Schafer
            YouTube Video Link: https://www.youtube.com/watch?v=th5_9woFJmk&t=3s
        """
        credentials = None
        # token.pickle stores the user's credentials from previously successful logins
        if os.path.exists("token.pickle"):
            print("Loading Credentials From File...")
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)
        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing Access Token...")
                credentials.refresh(Request())
            else:
                print("Fetching New Tokens...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_web_app.json",
                    scopes=[
                        "https://www.googleapis.com/auth/youtube",
                        "https://www.googleapis.com/auth/youtube.readonly",
                        "https://www.googleapis.com/auth/youtube.force-ssl",
                    ],
                )

                flow.run_local_server(
                    port=8080, prompt="consent", authorization_prompt_message=""
                )
                credentials = flow.credentials

                # Save the credentials for the next run
                with open("token.pickle", "wb") as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)
        youtube = build("youtube", "v3", credentials=credentials)
        return youtube

    def paginated_results(
        self, youtube_listable_resource, list_request, limit_requests=10
    ) -> Iterator:
        """Used to paginate results if data overflow; this iterates through web pages
        when there are more results on other pages to return."""
        remaining = -1 if limit_requests is None else limit_requests
        while list_request and remaining != 0:
            list_response = list_request.execute()
            yield list_response
            # see googleapiclient/discovery.py createNextMethod for *_next methods
            list_request = youtube_listable_resource.list_next(
                list_request, list_response
            )
            remaining -= 1
