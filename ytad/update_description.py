#!/bin/env python
"""Original Code: https://github.com/mCodingLLC/mCodingYouTube Functions to
update a single video description on YouTube."""

import difflib
import sys


class UpdateDescription:
    def __init__(self, youtube):
        self.youtube = youtube
        return

    def confirm_diff(self, old: str, new: str) -> bool:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< OLD <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(old)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> NEW  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(new)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< DIFF <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        differ = difflib.unified_diff(
            old.splitlines(keepends=True), new.splitlines(keepends=True)
        )
        sys.stdout.writelines(differ)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DONE")
        while True:
            decision = input("Does this look correct [Y/n]? ")
            decision = decision.lower()
            if decision == "" or "y" in decision:
                return True
            elif "n" in decision:
                return False
            print("Invalid input, try again")

    def update_description_on_youtube(self, video_id, new_description, verify) -> None:
        if "<" in new_description or ">" in new_description:
            raise ValueError("new_description cannot contain < or >")

        # see https://developers.google.com/youtube/v3/docs/videos/list
        videos_list_response = (
            self.youtube.videos().list(id=video_id, part="snippet").execute()
        )

        if not videos_list_response["items"]:
            raise KeyError(f"Video {video_id} was not found.")

        # Since the request specified a video ID, the response only contains one
        # video resource. This code extracts the snippet from that resource.
        videos_list_snippet = videos_list_response["items"][0]["snippet"]

        if videos_list_snippet["description"] == new_description:
            print(
                f"Video {video_id}: new description and old description are the same, skipping..."
            )
            return

        # comment this if statement if you are 100% comforatble with what you will be changing in the description.
        if (
            verify.lower() == "yes"
        ):  # if false, verify. Else, it will update all parameters.
            if not self.confirm_diff(
                old=videos_list_snippet["description"], new=new_description
            ):
                print("diff rejected, aborting program...")
                sys.exit(0)

        # user has confirmed the new version looks good, go ahead
        videos_list_snippet["description"] = new_description

        # it seems like a bug in the youtube api that this needs to be done
        # a downloaded video may have no tags,
        # but omitting tags during upload results in 400 error
        if "tags" not in videos_list_snippet:
            videos_list_snippet["tags"] = []

        # see https://developers.google.com/youtube/v3/docs/videos/update
        videos_update_response = (
            self.youtube.videos()
            .update(part="snippet", body=dict(snippet=videos_list_snippet, id=video_id))
            .execute()
        )

        if videos_update_response["snippet"]["description"] != new_description:
            raise RuntimeError("update failed")
