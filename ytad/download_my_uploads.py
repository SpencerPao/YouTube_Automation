#!/bin/env python
"""Original Code: https://github.com/mCodingLLC/mCodingYouTube Get Metadata
from ALL of the Video uploads on YouTube.

Important Pieces of Metadata to extract:     videoId     description
"""
import json
from typing import List
import pandas as pd
from time import gmtime, strftime


class DownloadUploadsData:
    def __init__(self, youtube):
        self.youtube = youtube
        return

    def _dump_json_to_file(self, obj, filename: str) -> None:
        """Write data to json file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(obj, f)

    def get_my_uploads_playlist_id(self) -> str:
        """Get the list of playlist ids from each youtube video."""
        # see https://developers.google.com/youtube/v3/docs/channels/list
        channels_response = (
            self.youtube.channels().list(mine=True, part="contentDetails").execute()
        )

        for channel in channels_response["items"]:
            return channel["contentDetails"]["relatedPlaylists"]["uploads"]

        return None

    def download_playlist_video_snippets(self, playlist_id, file_prefix, auth) -> None:
        """Get playlist data from YouTube Channel.
        Parameters:
        ----------
        playlist_id: str
            Playlist id for each YouTube Video.
        file_prefix: str
            Starting filename for data referenced files in /data/
        auth:
            YouTube Credentials for API reference for your YouTube account.
        Return:
        ----------"""
        # see https://developers.google.com/youtube/v3/docs/playlistItems/list
        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=playlist_id, part="snippet", maxResults=50
        )

        results = auth.paginated_results(
            self.youtube.playlistItems(), playlistitems_list_request
        )
        for page_no, playlistitems_list_response in enumerate(results):
            self._dump_json_to_file(
                playlistitems_list_response, f"{file_prefix}{page_no}.json"
            )

    def get_videos_from_json_files(self, files: List[str]) -> List[str]:
        """Gets videos from list of files.
        Parameters:
        ----------
        files: List[str]
            List of filenames that contain data references.
        Return:
        ----------
        List[str]:
            List of items related to videos.
        """
        videos = []
        for filename in files:
            with open(filename, "r", encoding="utf-8") as f:
                playlist_list_response = json.load(f)
                videos.extend(playlist_list_response["items"])
        return videos

    def download_like_dislike(self, channel_id, auth) -> None:
        """Get the current likes and dislikes of each YouTube Video.
        Parameters:
        ---------
        channel_id: str
            Your YouTube Channel ID.
        auth:
            YouTube Credentials for API reference for your YouTube account.
        Return:
        ---------
        None
        """
        requestVidId = self.youtube.search().list(
            part="snippet", channelId=channel_id, order="date", maxResults=50
        )
        results = auth.paginated_results(self.youtube.search(), requestVidId)
        video_names = []
        video_ids = []
        likes = []
        dislikes = []
        ratios = []
        date_stores = []
        c = 1
        for page_no, requestVidId_response in enumerate(results):
            for item in requestVidId_response["items"]:
                try:
                    vidId = item["id"]["videoId"]
                    title = item["snippet"]["title"]
                    # Get statistics
                    requestStats = self.youtube.videos().list(
                        part="statistics", id=vidId
                    )
                    responseStats = requestStats.execute()

                    # Like Dislike.
                    for item in responseStats["items"]:
                        like = item["statistics"]["likeCount"]
                        dislike = item["statistics"]["dislikeCount"]

                    ratio = float(like) / (float(like) + float(dislike)) * 100
                    currentDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    video_names.append(title)
                    video_ids.append(vidId)
                    likes.append(like)
                    dislikes.append(dislike)
                    ratios.append(ratio)
                    date_stores.append(currentDate)
                    print(
                        c,
                        "Video Name",
                        title,
                        "Video ID ",
                        item["id"],
                        like,
                        dislike,
                        ratio,
                        "Date Updated:",
                        currentDate,
                        "GMT",
                    )
                    c += 1
                except Exception:
                    print("Ignoring playlist pull..")
                    continue
        video_names = pd.DataFrame(video_names)
        video_ids = pd.DataFrame(video_ids)
        likes = pd.DataFrame(likes)
        dislikes = pd.DataFrame(dislikes)
        ratios = pd.DataFrame(ratios)
        date_stores = pd.DataFrame(date_stores)
        df = pd.concat(
            [video_names, video_ids, likes, dislikes, ratios, date_stores], axis=1
        )
        df.columns = ["Video_Names", "Video_IDs", "Likes", "Dislikes", "Ratios", "Date"]
        df.to_csv("data/video_statistics.csv", mode="w+", index=False)
        return None
