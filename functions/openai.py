import requests
import json

from functions import text

api_key = "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"


def chatGPT(text, max_tokens=100):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        "max_tokens": max_tokens
    }
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers,
                             data=json.dumps(data))

    answer = response.json()
    print(answer)
    answer_text = answer["choices"][0]["message"]["content"]
    print(answer_text)
    answer_text = text.format_text(answer_text)
    print(answer_text)
    return answer_text


def title_description(body, title_tokens=100, description_tokens=300):
    body = text.format_text(body)
    question_title = "(don't use words such as death, suicide, ...)(Answer with just the title, max: 10 words) Create a clickbait for a youtube video where the text is the following: " + body
    video_title = chatGPT(question_title, title_tokens)
    question_description = "(don't use words such as death, suicide, ...)(Answer with just the description, max: 30 words, and the hashtags separated by one space and with an # before the world: max: 3 words. Remember the strcture: description, #hashtag1 #hashtag2 #hashtag3) Create a 100 character long description and 3 hashtags of the video with the following text: " + body
    video_description = chatGPT(question_description, description_tokens) + "\nComment with your opinions, follow the channel, hit the like button and share if you enjoyed the video"

    return video_title, video_description


def gender(body):
    body = text.format_text(body)
    question_gender = "(Answer with just one of the following words: 'male', 'female') the following text has been written by a man or a woman? " + body
    video_gender = chatGPT(question_gender, 20)

    if "female" in video_gender:
        return 'en_us_001'
    return 'en_us_006'
