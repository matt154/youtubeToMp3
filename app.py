from datetime import datetime

from apiclient.discovery import build
from pytube import YouTube
import os

DEVELOPER_KEY = "AIzaSyBYVoaKQFFgha2kITO7fHQNzxdiU8VIc7I"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube_url_format = "https://www.youtube.com/watch?v="


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        pass
    else:
        print("Successfully created the directory %s " % path)


def download_video(video_url, path_to_download):
    create_dir(path_to_download)

    return YouTube(video_url).streams.filter(only_audio=True).first().download(path_to_download)

def get_from_play_list(playlist_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    res = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults="1"
    ).execute()
    next_page_token = res.get('nextPageToken')

    while 'nextPageToken' in res:
        nextPage = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults="50",
            pageToken=next_page_token
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            next_page_token = nextPage['nextPageToken']

    return res


def get_videos_id(videos_dict):
    ids = []
    for video in videos_dict["items"]:
        ids.append(video["snippet"]["resourceId"]["videoId"])

    return ids


def download_playlist(video_url, to_path):
    play_list_id = video_url.split("=")[-1]
    for videoId in get_videos_id(get_from_play_list(play_list_id)):
        print(download_video(youtube_url_format + videoId, to_path))


def set_directory(dir_name):
    if len(dir_name) == 0:
        dir_name = datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace("/", "-")

    if not os.path.isabs(dir_name):
        dir_name = os.path.join(os.getcwd(), "music", dir_name)

    return dir_name


def change_extensions_to_mp3(path):
    print("change")
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        os.rename(file_path, file_path.replace(".mp4", ".mp3"))


def main():
    to_continue = True
    while to_continue:
        print("1. video")
        print("2. playlist")
        print("3. exit")

        code = input("Enter your choice: ")
        options = ["1", "2", "3"]
        while code not in options:
            code = input("Invalid input!\nEnter tour choice: ")
        int_code = int(code)

        if int_code == 1:
            url = input("Enter the video url: ")
            directory = input("What the name of directory you want to save in it: ")
            clips_path = set_directory(directory)
            file_path = download_video(url, clips_path)
            os.rename(file_path, file_path.replace(".mp4", ".mp3"))
        if int_code == 2:
            url = input("Enter the playList url: ")
            directory_name = input("What the name of directory you want to save in it: ")
            clips_path = set_directory(directory_name)
            download_playlist(url, clips_path)
            change_extensions_to_mp3(clips_path)
        if int_code == 3:
            to_continue = False


if __name__ == "__main__":
    main()
