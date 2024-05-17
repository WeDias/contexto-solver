from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import requests

from src.config import ALL_EN_WORDS_PATH, VALID_WORDS_PATH, INVALID_WORDS_PATH, CONTEXTO_API_URL


start_at = datetime.now()
valid_words = set()
invalid_words = set()
all_en_words = set(open(ALL_EN_WORDS_PATH).read().splitlines())


def process_word(word: str) -> None:
    response = requests.get(f'{CONTEXTO_API_URL}/en/game/606/{word}')
    
    if response.ok:
        valid_words.add(response.json()['lemma'])
    else:
        invalid_words.add(word)
    
    time_elapsed = datetime.now() - start_at
    processed_words = len(valid_words) + len(invalid_words)

    print(time_elapsed, processed_words, word, response.status_code)


if __name__ == '__main__':

    with ThreadPoolExecutor(max_workers=128) as executor:
        tuple(executor.map(process_word, all_en_words))

    with open(VALID_WORDS_PATH, 'w') as file:
        file.write('\n'.join(sorted(valid_words)))

    with open(INVALID_WORDS_PATH, 'w') as file:
        file.write('\n'.join(sorted(invalid_words)))
