import requests
import base64
import io
import pydub
import json

API_BASE_URL = "https://api16-normal-c-useast2a.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = ("com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; "
              "Build/NRD90M;tt-ok/3.12.13.1)")


def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech"):
    req_text = req_text.replace("\n", "")
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    req_text = req_text.replace("ä", "ae")
    req_text = req_text.replace("ö", "oe")
    req_text = req_text.replace("ü", "ue")
    req_text = req_text.replace("ß", "ss")
    req_text = req_text.replace("AITA","Am I the asshole ")

    r = requests.post(
        f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233",
        headers={
            'User-Agent': USER_AGENT,
            'Cookie': f'sessionid={session_id}'
        }
    )

    try:
        r.json()
    except json.decoder.JSONDecodeError:
        output_data = {"status": "Invalid JSON response", "status_code": 6}
        print(output_data, "skipped post", "req_text: ",req_text)
        return output_data

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data, "skipped post")
        return output_data

    vstr = r.json()["data"]["v_str"]
    msg = r.json()["message"]
    scode = r.json()["status_code"]
    log = r.json()["extra"]["log_id"]
    dur = r.json()["data"]["duration"]
    spkr = r.json()["data"]["speaker"]

    b64d = base64.b64decode(vstr)
    audio_data = io.BytesIO(b64d)
    audio_segment = pydub.AudioSegment.from_file(audio_data)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    output_data["audio_segment"] = audio_segment

    return output_data
