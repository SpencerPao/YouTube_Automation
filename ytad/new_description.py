#!/bin/env python
"""Original Code:
https://github.com/mCodingLLC/mCodingYouTube/tree/master/mcoding_youtube.

This is where you can edit what description your videos will be. For now, I will just create
the ability to update the like and dislike counter.

There is already a lot of good code here, so I will leave most of it here.
"""
from datetime import datetime
from pytz import timezone, utc
import pandas as pd


class NewDescription:
    def __init__(self):
        pass

    def _get_time(self, time_zone: str) -> None:
        """Get current time; supports est/pst.
        time_zone: str
            est or pst
        Parameters:
        ----------
        time_zone: str
            type of time zone standard you want to include for your timestamp.
        Return:
        ----------
        None"""
        date_format = "%m-%d-%Y %H:%M:%S %Z"
        date = datetime.now(tz=utc)
        if time_zone.lower() == "pst":
            date = date.astimezone(timezone("US/Pacific"))
            pstDateTime = date.strftime(date_format)
            return pstDateTime
        elif time_zone.lower() == "est":
            date = date.astimezone(timezone("US/Eastern"))
            estDateTime = date.strftime(date_format)
            return estDateTime
        return None

    def merge_metadata_description(self, old_description: str, record: pd.DataFrame, time_zone: str) -> str:
        """Update new description with the number of likes, dislikes, ratios, and time stamps.
        Parameters:
        ----------
        old_description: str
            old description of your YouTube Videos.
        record: pd.DataFrame
            the dataframe that holds metadata for each of your videos.
        timezone: str
            the timezone to be plugged in for timestamp. Supports EST/PST.
        Return:
        ----------
        str:
            new description to be updated.
        """
        current_dt = self._get_time(time_zone)  # Pst
        likes = record["Likes"].values[0]
        dislikes = record["Dislikes"].values[0]
        if likes == 0 and dislikes == 0:
            return old_description
        else:
            edit_line = f"===== Likes: {likes} 👍: Dislikes: {dislikes} 👎: {round(int(likes)/(int(likes) + int(dislikes)) * 100, 3)}% : Updated on {current_dt} ====="
            if old_description.startswith("====="):
                # Update the counter.
                edit_desc = old_description.splitlines()
                edit_desc[0] = edit_line
                edit_desc = "\n".join(edit_desc)
                return edit_desc
            else:
                # insert counter line.
                edit_line = edit_line + "\n" + old_description
                return edit_line
