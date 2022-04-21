"""Run via command line to update your like to dislike ratio in YouTube
comment descriptions."""
import argparse
from dotenv import load_dotenv
import pandas as pd
from ytad.app_config import Config
from ytad.download_my_uploads import DownloadUploadsData
from ytad.authentication import Authenticate
from ytad.authentication import Authenticate
from ytad.new_description import NewDescription
from ytad.update_description import UpdateDescription
import glob
import os
import boto3
from datetime import datetime
from pytz import timezone, utc


def upload_aws_bucket(
    file_source_path: str = "data/video_statistics.csv",
    aws_bucket_name: str = "youtubedescription",
) -> None:
    """
    Sending description files to bucket for storage.
    Parameters:
    ----------
    file_source_path: str
        Address of file you want to save.
    Return:
    ----------
    None
    """
    s3 = boto3.resource("s3")
    date_format = "mdy_%m_%d_%Y_hms_%H_%M_%S_%Z"
    date = datetime.now(tz=utc)
    date = date.astimezone(timezone("US/Eastern"))
    estDateTime = date.strftime(date_format)
    s3.meta.client.upload_file(
        file_source_path,  # file to send to s3.
        aws_bucket_name,  # bucketname
        "video_statistics_{}.csv".format(estDateTime),
    )  # new name of file.


def update(args: argparse.ArgumentParser) -> None:
    """Update YouTube description with most up to date like to dislikes using YouTube's Data API v3."""
    load_dotenv()
    config = Config(os.getenv("CLIENT_SECRET_FILE"), os.getenv("CHANNEL_ID"))
    channel_id = config.CHANNEL_ID
    print("Verifying your API keys...")
    auth = Authenticate()
    youtube_id = auth.check_token_web_app_data_api()
    dmu = DownloadUploadsData(youtube=youtube_id)

    print("Repull data from YouTube?", args.update_df, type(args.update_df))
    if args.update_df.lower() == "yes":
        uploads_playlist_id = dmu.get_my_uploads_playlist_id()
        file_prefix = "data/my_videos_page_"
        if not os.path.exists('data'):
            os.makedirs('data')
        if uploads_playlist_id is not None:
            dmu.download_playlist_video_snippets(
                playlist_id=uploads_playlist_id, file_prefix=file_prefix, auth=auth
            )
        else:
            print("There is no uploaded videos playlist for this user.")
        # ------------------------------------------------------------------------------------------
        # Obtaining the likes and dislikes from YouTube API
        files = glob.glob("data/my_videos_page_*.json")
        videos = dmu.get_videos_from_json_files(files=files)
        print(f"Number of records; loaded {len(videos)}")

        if uploads_playlist_id is not None:
            dmu.download_like_dislike(
                channel_id=channel_id, auth=auth
            )
        else:
            print("There is no uploaded videos playlist for this user.")
    else:
        files = glob.glob("data/my_videos_page_*.json")
        videos = dmu.get_videos_from_json_files(files=files)

    # ------------------------------------------------------------------------------------------
    # Update Description for each YouTube video.
    video_stat = pd.read_csv("data/video_statistics.csv")
    print("Loading video statistics")
    print(video_stat)

    def updated_description(old_description: str, record: pd.DataFrame) -> str:
        ud = NewDescription()
        return ud.merge_metadata_description(old_description, record, args.tz)

    new_descriptions = {
        v["snippet"]["resourceId"]["videoId"]: updated_description(
            v["snippet"]["description"],
            video_stat.loc[
                video_stat["Video_IDs"] == v["snippet"]["resourceId"]["videoId"]
            ],
        )
        for v in videos
    }

    if input("Start update process (must type YES)? ") != "YES":
        return
    upd = UpdateDescription(youtube=youtube_id)
    for video_id, new_description in new_descriptions.items():
        upd.update_description_on_youtube(
            video_id=video_id,
            new_description=new_description,
            verify=args.verify_each_update,
        )
        print(
            f"Video ID: {video_id} has been updated -- Check out updated description."
        )
    if args.aws.lower() == "yes":
        print(f"Saving files to s3: {args.bucket}")
        upload_aws_bucket(aws_bucket_name=args.bucket)


# if __name__ == "__main__":
def update_video_descriptions():
    """Pass in arguments to command line to execute update command.
    Example: python update_notifications.py --update_df=No --verify_each_update=yes"""
    parser = argparse.ArgumentParser(
        description="Inputs arguments to update YouTube Description with like to dislike ratio."
    )
    parser.add_argument(
        "--update_df",
        type=str,
        default="yes",
        required=False,
        help="If you already have most up to date dataframs in /data/, you can conserve number of requests by opting out. Yes/No",
    )
    parser.add_argument(
        "--verify_each_update",
        type=str,
        default="yes",
        required=False,
        help="Update YouTube video descriptions without verifying content? Yes/No",
    )
    parser.add_argument(
        "--aws",
        type=str,
        default="no",
        required=False,
        help="Set --aws=yes if you want to run this on an instance. This sends data file to S3 bucket.",
    )
    parser.add_argument(
        "--bucket",
        type=str,
        default="youtubedescription",
        required=False,
        help="If --aws=yes, then this argument will be the bucket name. --bucket=youtubedescription",
    )
    parser.add_argument(
        "--tz",
        type=str,
        default="est",
        required=False,
        help="Supports est or pst timezones.",
    )
    args = parser.parse_args()
    update(args)
