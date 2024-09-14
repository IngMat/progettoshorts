import re


def format_text(text):
    text = text.replace("\n", "")
    text = text.replace(".", "")
    text = text.replace("\"", "")
    text = text.replace("'", "")
    text = text.replace("\\", "")
    text = text.replace("?", "")
    return text


def divide_by_words(phrases: [str], num_words: int):
    sentences = []
    for block in phrases:
        blocks = block.split()  # split by spaces
        if len(blocks) < num_words:  # short block
            sentences.append(block)
            continue
        piece = len(blocks) // num_words + 1
        already_taken = 0
        for i in range(piece):
            if i == piece - 1:
                sentences.append(' '.join(blocks[already_taken:]))  # appended the last block
            else:
                sentences.append(' '.join(blocks[already_taken: already_taken + len(
                    blocks) // piece]))  # unione parole in più pezzi accettati da tiktok
                already_taken += len(blocks) // piece
    return sentences


def divide_by_punctuation(text: str, *args):
    char_to_split = "[({}).:;!?]"  # inside []
    phrases = re.split(char_to_split, text.strip())  # split by punctuation

    for arg in args:  # append any passed string
        if isinstance(arg, str):
            phrases.append(arg)

    divided_by_words = divide_by_words(phrases, 40)
    return divided_by_words


def multiline_string(text, line_words):
    words = text.split()
    formatted = '\n'.join([' '.join(words[i:i + line_words]) for i in range(0, len(words), line_words)])
    return formatted
