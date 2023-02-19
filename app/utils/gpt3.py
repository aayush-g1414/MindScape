from math import ceil


def num_of_tokens(text):
    return ceil(0.65 * len(text.split(' ')))


def chunkify(max_token_size, text):
    chunks = []
    text = text.split('\n')

    current_num_tokens = 0
    current_chunk = ' '

    for line in text:
        if num_of_tokens(line) + current_num_tokens > max_token_size:
            chunks.append(current_chunk)
            current_num_tokens = 0
            current_chunk = ''
        else:
            current_num_tokens += num_of_tokens(line)
            if current_chunk == ' ':
                current_chunk += line
            else:
                current_chunk += '. '+line

    if current_chunk != ' ':
        chunks.append(current_chunk)

    return chunks