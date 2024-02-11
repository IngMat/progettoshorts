import sys
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import argparse
import http.client
import time

from functions import times

# Definisci le costanti per l'autenticazione
CLIENT_SECRETS_FILE = "./client_secrets.json"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
MISSING_CLIENT_SECRETS_MESSAGE = "Please configure your client_secrets.json file."

# Un insieme di codici di stato HTTP che dovrebbero essere ritentati.
RETRIABLE_STATUS_CODES = {500, 502, 503, 504}

# Un insieme di eccezioni che dovrebbero essere ritentate.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)

# Numero massimo di tentativi di caricamento prima di terminare.
MAX_RETRIES = 10


def get_authenticated_service(arguments):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    storage = Storage(f"{sys.argv[0]}-oauth2.json")
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, arguments)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube_el, options, week_day):

    body = {
        "snippet": {
            "title": options.title,
            "description": options.description,
            "tags": None,
            "categoryId": options.category
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": times.publish_time(week_day),
            "selfDeclaredMadeForKids": False
        }
    }

    # Inserisci il file video
    media_body = MediaFileUpload(options.file, chunksize=-1, resumable=True)
    if not media_body.size():
        print("Il file specificato non esiste.")
        return

    # Crea una richiesta di inserimento di YouTube
    insert_request = youtube_el.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media_body
    )

    # Esegui la richiesta
    video_link = resumable_upload(insert_request)

    return video_link


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Caricamento del file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(f"Video caricato con successo, ID video: {response['id']}")
                    return "https://www.youtube.com/watch?v=" + response["id"]
                else:
                    exit("La risposta non contiene un ID video.")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"Errore HTTP {e.resp.status}:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"Errore:\n{e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("Nessun tentativo di ripetizione riuscito, esco.")
            sleep_seconds = 2 * retry
            print(f"Riposo {sleep_seconds} secondi e riprovo...")
            time.sleep(sleep_seconds)
            error = None


def upload_video(video_path, video_title, video_description, week_day):

    args = argparse.Namespace()
    args.file = video_path
    args.title = video_title
    args.description = video_description
    args.keywords = None
    args.category = "22"
    args.privacyStatus = "private"
    args.logging_level = "INFO"
    args.noauth_local_webserver = True

    youtube = get_authenticated_service(args)
    video_link = initialize_upload(youtube, args, week_day)

    return video_link
