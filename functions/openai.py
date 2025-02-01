import requests
import json
from functions import text


def chatGPT(text, max_tokens=100):
    with open("keys.txt", 'r') as keys_file:
        lines = keys_file.readlines()
    # Prepare the HTTP headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {lines[2].rstrip}"
    }

    # Define the request payload
    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        "max_tokens": max_tokens
    }

    # Send a POST request to the OpenAI API and retrieve the response
    response = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers,
                             data=json.dumps(data))

    # Extract and format the response content
    answer = response.json()
    print(answer)
    answer_text = answer["choices"][0]["message"]["content"]
    print(answer_text)
    answer_text = text.format_text(answer_text)
    print(answer_text)
    return answer_text


def title_description(body, title_tokens=100, description_tokens=300):
    # Generates a video title and description based on the given text
    body = text.format_text(body)
    question_title = "(don't use words such as death, suicide, ...)(Answer with just the title, max: 10 words) Create a clickbait for a youtube video where the text is the following: " + body
    video_title = chatGPT(question_title, title_tokens)
    question_description = "(don't use words such as death, suicide, ...)(Answer with just the description, max: 30 words, and the hashtags separated by one space and with an # before the world: max: 3 words. Remember the strcture: description, #hashtag1 #hashtag2 #hashtag3) Create a 100 character long description and 3 hashtags of the video with the following text: " + body
    video_description = chatGPT(question_description, description_tokens) + "\nComment with your opinions, follow the channel, hit the like button and share if you enjoyed the video"

    return video_title, video_description


def gender(body):
    # determines the likely gender of the author of the given text.
    body = text.format_text(body)
    question_gender = "(Answer with just one of the following words: 'male', 'female') the following text has been written by a man or a woman? " + body
    video_gender = chatGPT(question_gender, 20)

    # Map the result to a TikTok voi