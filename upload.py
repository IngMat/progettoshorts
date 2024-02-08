import os
import sys
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from typing import TypedDict, List, Union


class VideoOptions(TypedDict):
    keywords: str
    title: str
    description: str
    category: str
    privacyStatus: str
    file: str


# Definisci le costanti per l'autenticazione
CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
MISSING_CLIENT_SECRETS_MESSAGE = "Please configure your client_secrets.json file."


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(f"{sys.argv[0]}-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION)  # non necessario avere un proprio http penso
    #  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube, options):
    tags = options.get("keywords", "").split(",")

    body = {
        "snippet": {
            "title": options["title"],
            "description": options["description"],
            "tags": tags,
            "categoryId": options["category"]
        },
        "status": {
            "privacyStatus": options["privacyStatus"]
        }
    }


if __name__ == "__main__":
    # Imposta gli argomenti per l'upload del video
    video_options = {
        "file": "output/video_with_audio 0.mp4",
        "title": "prova",
        "description": "chiederemo a chatgpt",
        "keywords": "surfing, Santa Cruz",
        "category": "22",  # Categoria People & Blogs
        "privacyStatus": "private"  # Stato di privacy (public, private, unlisted)
    }

    youtube = get_authenticated_service(video_options)
    initialize_upload(youtube, video_options)
