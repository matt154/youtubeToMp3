import json
import os
from apiclient.discovery import build
from pytube import YouTube
from moviepy.editor import *
from pathlib import Path
from datetime import datetime

DEVELOPER_KEY = "AIzaSyBYVoaKQFFgha2kITO7fHQNzxdiU8VIc7I"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube_url_format = "https://www.youtube.com/watch?v="


def create_dir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)

def downloadVideo(video_url, path_to_download=".\\videos"):
    create_dir(path_to_download)

    return YouTube(video_url).streams.first().download(".\\videos")



def convert_MP4_to_mp3_dir(path_from=".\\videos", path_to=".\\audio"):
    file_names = os.listdir(path_from)
    create_dir(path_to)

    for file_name in file_names:
        file_dest_path = os.path.join(path_to, file_name[:-1] + "3")
        if not os.path.exists(file_dest_path):
            VideoFileClip(os.path.join(path_from, file_name)).audio.write_audiofile(file_dest_path)
    
    return 0

def convert_MP4_to_mp3(file_name, path_to=".\\audio"):
    create_dir(path_to)
    VideoFileClip(file_name).audio.write_audiofile(os.path.join(path_to, file_name.split("\\")[-1][:-1] + "3"))


# convert_MP4_to_mp3()

def getFromPlaylist(playlistId):
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    res = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlistId,
    maxResults="1"
    ).execute()
    nextPageToken = res.get('nextPageToken')

    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    return res

def getVideosId(videosDict):
    ids = []
    for video in videosDict["items"]:
        ids.append(video["snippet"]["resourceId"]["videoId"])

    return ids




# print(json.dumps(getFromPlaylist("PLNMKyY61jz91C89ijqITKyJfvg3sjOkql"), indent=6))
# print(getFromPlaylist("PLNMKyY61jz91C89ijqITKyJfvg3sjOkql")["items"][0]["snippet"]["resourceId"]["videoId"])
def downloadPlaylist(videoUrl):
    playListId = videoUrl.split("=")[-1]
    for videoId in getVideosId(getFromPlaylist(playListId)):
        print(downloadVideo(youtube_url_format + videoId))

def main():
    toContinue = True
    while toContinue:
        print("1. video")
        print("2. playlist")
        print("3. exit")
        
        code = input("Enter your choice: ")
        options = ["1","2","3"]
        while not code in options:
            code = input("Invalid input!\nEnter tour choice: ")
        intCode = int(code)

        if intCode == 1:
            convert_MP4_to_mp3(downloadVideo(input("Enter the video url: ")))
        if intCode == 2:
            downloadPlaylist(input("Enter the playList url: "))
            convert_MP4_to_mp3_dir()
        if intCode == 3:
            toContinue = False



if __name__ == "__main__":
    main()

