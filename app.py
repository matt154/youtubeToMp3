import json
import os
from apiclient.discovery import build
from pytube import YouTube
from moviepy.editor import *
from pathlib import Path
import os

DEVELOPER_KEY = "AIzaSyBYVoaKQFFgha2kITO7fHQNzxdiU8VIc7I"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube_url_format = "https://www.youtube.com/watch?v="

video_dir = ""
audio_dir = ""


def create_dir(path):
    try:
        os.mkdir(path)
    except OSError:
        pass
    else:
        print("Successfully created the directory %s " % path)


def downloadVideo(video_url, path_to_download):
    create_dir(path_to_download)

    return YouTube(video_url).streams.first().download(path_to_download)


def convert_MP4_to_mp3_dir(path_from, path_to):
    file_names = os.listdir(path_from)
    create_dir(path_to)

    for file_name in file_names:
        file_dest_path = os.path.join(path_to, file_name[:-1] + "3")
        if not os.path.exists(file_dest_path):
            VideoFileClip(os.path.join(path_from, file_name)).audio.write_audiofile(file_dest_path)

    return 0


def convert_MP4_to_mp3(file_name, path_to):
    create_dir(path_to)
    VideoFileClip(file_name).audio.write_audiofile(os.path.join(path_to, file_name.split("\\")[-1][:-1] + "3"))


# convert_MP4_to_mp3()

def getFromPlaylist(playlistId):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
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
        print(downloadVideo(youtube_url_format + videoId, video_dir))


def setDirectorys(dir_name):
    global audio_dir
    global video_dir

    if dir_name[-1] == "\\" or dir_name[-1] == "/":
        audio_dir = dir_name + "audio"
        video_dir = dir_name + "video"
    elif len(dir_name) == 0:
        audio_dir = ".\\" + "audio"
        video_dir = ".\\" + "video"
    else:
        audio_dir = dir_name + "\\audio"
        video_dir = dir_name + "\\video"

    if not os.path.isabs(audio_dir):
        audio_dir = ".\\music\\" + audio_dir
    if not os.path.isabs(video_dir):
        video_dir = ".\\music\\" + video_dir


def main():
    toContinue = True
    while toContinue:
        print("1. video")
        print("2. playlist")
        print("3. exit")

        code = input("Enter your choice: ")
        options = ["1", "2", "3"]
        while code not in options:
            code = input("Invalid input!\nEnter tour choice: ")
        intCode = int(code)

        if intCode == 1:
            url = input("Enter the video url: ")
            setDirectorys(input("What the name of directory you want to save in it: "))
            convert_MP4_to_mp3(downloadVideo(url, video_dir), audio_dir)
        if intCode == 2:
            downloadPlaylist(input("Enter the playList url: "))
            setDirectorys(input("What the name of directory you want to save in it: "))
            convert_MP4_to_mp3_dir(video_dir, audio_dir)
        if intCode == 3:
            toContinue = False


if __name__ == "__main__":
    main()
