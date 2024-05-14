import numpy as np
import gensim.downloader as downloader

from src.config import WORDS_FILE_PATH, WORDS_EMBEDDINGS_PATH, WORDS_FILTERED_PATH


def main():
    model = downloader.load('word2vec-google-news-300')

    with open(WORDS_FILE_PATH) as file:
        words = [word.strip().lower() for word in file]

    filtered_words = [word for word in words if word in model]
    words_embeddings = np.stack([model[word] for word in filtered_words if word in model])

    np.save(WORDS_EMBEDDINGS_PATH, words_embeddings)
    
    with open(WORDS_FILTERED_PATH, 'w') as file:
        file.write('\n'.join(filtered_words))


if __name__ == '__main__':
    main()
