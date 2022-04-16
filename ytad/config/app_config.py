"""
    Configuration file for downloaded client secret file when creating the OAuth2
    credentials from google cloud.
"""


class Config:
    def __init__(self, client_secret_file: str, user: str):
        self.client_secret_file: str = client_secret_file
        self.CHANNEL_ID = user
