import os


WIN_SCORE = 1
CONTEXTO_URL = 'https://contexto.me/'
CONTEXTO_API_URL = 'https://api.contexto.me/machado/'

DATA_FOLDER_NAME = 'data'
CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, DATA_FOLDER_NAME)

ALL_EN_WORDS_FILE = 'all-en-words.txt'
ALL_EN_WORDS_PATH = os.path.join(DATA_DIR, ALL_EN_WORDS_FILE)

COMMON_WORDS_FILE = 'common-words.txt'
COMMON_WORDS_PATH = os.path.join(DATA_DIR, COMMON_WORDS_FILE)

WORDS_EMBEDDINGS_FILE = 'embeddings.npy'
WORDS_EMBEDDINGS_PATH = os.path.join(DATA_DIR, WORDS_EMBEDDINGS_FILE)

INVALID_WORDS_FILE = 'invalid-words.txt'
INVALID_WORDS_PATH = os.path.join(DATA_DIR, INVALID_WORDS_FILE)

VALID_WORDS_FILE = 'valid-words.txt'
VALID_WORDS_PATH = os.path.join(DATA_DIR, VALID_WORDS_FILE)

WORDS_FILTERED_FILE = 'words-filtered.txt'
WORDS_FILTERED_PATH = os.path.join(DATA_DIR, WORDS_FILTERED_FILE)
