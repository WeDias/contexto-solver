import os


CONTEXTO_URL = 'https://contexto.me/'

START_GUESS = 'animal'
WORDS_FILE = 'words.txt'
BLACK_LIST_FILE = 'blacklist.txt'
WORDS_EMBEDDINGS_FILE = 'embeddings.npy'
WORDS_FILTERED_FILE = 'words-filtered.txt'
DATA_FOLDER_NAME = 'data'

CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, DATA_FOLDER_NAME)

WORDS_FILE_PATH = os.path.join(DATA_DIR, WORDS_FILE)
BLACK_LIST_PATH = os.path.join(DATA_DIR, BLACK_LIST_FILE)
WORDS_EMBEDDINGS_PATH = os.path.join(DATA_DIR, WORDS_EMBEDDINGS_FILE)
WORDS_FILTERED_PATH = os.path.join(DATA_DIR, WORDS_FILTERED_FILE)

WIN_SCORE = 1
MAX_SCORE = 100_000
