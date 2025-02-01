import re


def format_text(text):
    # Cleans a given text by removing certain characters
    text = text.replace("\n", "")
    text = text.replace(".", "")
    text = text.replace("\"", "")
    text = text.replace("'", "")
    text = text.replace("\\", "")
    text = text.replace("?", "")
    return text


def divide_by_words(phrases: [str], num_words: int):
    # Split a list oh phrases into smaller segments based on word count
    sentences = []
    for block in phrases:
        blocks = block.split()  # split by spaces
        if len(blocks) < num_words:  # short block
            sentences.append(block)
            continue
        piece = len(blocks) // num_words + 1 # calculate number of segments
        already_taken = 0
        for i in range(piece):
            if i == piece - 1:
                # Append the last block with the remaining words
                sentences.append(' '.join(blocks[already_taken:]))
            else:
                # Append a block of words ensuring even distribution
                sentences.append(' '.join(blocks[already_taken: already_taken + len(
                    blocks) // piece]))
                already_taken += len(blocks) // piece
    return sentences


def divide_by_punctuation(text: str, *args):
    # Splits a text into sentences using punctuation and then further divides it by words
    char_to_split = "[({}).:;!?]"
    phrases = re.split(char_to_split, text.strip())  # split by punctuation

    for arg in args:  # append addition strings if provided
        if isinstance(arg, str):
            phrases.append(arg)

    divided_by_words = divide_by_words(phrases, 40)
    return divided_by_words


def multiline_string(text, line_words):
    # Format a string into multiple lines
    words = text.split()
    formatted = '\n'.join([' '.join(words[i:i + line_words]) for i in range(0, len(words), line_words)])
    return formatted
