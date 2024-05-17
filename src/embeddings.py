from concurrent.futures import ThreadPoolExecutor
import numpy as np
import gensim.downloader as downloader

from src.words_generator import process_word, valid_words
from src.config import COMMON_WORDS_PATH, WORDS_EMBEDDINGS_PATH, FILTERED_WORDS_PATH


if __name__ == '__main__':

    model = downloader.load('word2vec-google-news-300')

    with open(COMMON_WORDS_PATH) as file:
        words = [word.strip().lower() for word in file]
        
    with ThreadPoolExecutor(max_workers=128) as executor:
        tuple(executor.map(process_word, words))

    filtered_words = [word for word in valid_words if word in model]
    words_embeddings = np.stack([model[word] for word in filtered_words if word in model])

    np.save(WORDS_EMBEDDINGS_PATH, words_embeddings)
    
    with open(FILTERED_WORDS_PATH, 'w') as file:
        file.write('\n'.join(filtered_words))
