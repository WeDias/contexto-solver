import random
from time import sleep

import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from selenium import webdriver
from selenium.webdriver.common.by import By

from src.config import WORDS_EMBEDDINGS_PATH, FILTERED_WORDS_PATH, WIN_SCORE


class Solver:

    def __init__(self, web_driver: webdriver.Chrome, sleep_time: float) -> None:
        self.game_finished: bool = False
        self.word_input = None
        self.web_driver = web_driver
        self.sleep_time = sleep_time
        self.results = []
        self.word_to_distances = {}
        self.embeddings = np.load(WORDS_EMBEDDINGS_PATH)
        self.words = list(map(str.strip, open(FILTERED_WORDS_PATH).readlines()))
        
    def get_distances(self, word: str) -> np.ndarray:
        try:
            word_id = self.words.index(word)
        except ValueError:
            return None
        return cosine_distances([self.embeddings[word_id]], self.embeddings)[0]

    def get_word_to_distances(self, guesses: list[tuple[str, int]]) -> dict[str, np.ndarray]:
        word_to_distances = {}
        for word, _ in guesses:
            dists = self.get_distances(word)
            if dists is not None:
                word_to_distances[word] = dists
        return word_to_distances

    def add_result(self, word, order) -> None:
        self.results.append((word, order))
        self.word_to_distances[word] = self.get_distances(word)

    def get_score(self, guesses, word_to_distances, min_gap=0.1, num_samples=500) -> np.ndarray:
        scores = np.zeros(len(self.words))
        for _ in range(0, num_samples):
            word_a, order_a = random.choice(guesses)
            word_b, order_b = random.choice(guesses)

            if order_a < order_b * (1.0 - min_gap):
                scores += (word_to_distances[word_a] - word_to_distances[word_b] < 0)
            if order_a > order_b * (1.0 + min_gap):
                scores += (word_to_distances[word_a] - word_to_distances[word_b] > 0)

        return scores

    def best_scores(self, guesses, word_to_distances, top: int) -> np.ndarray:
        best_guess_word, _ = sorted(guesses, key=lambda x: x[1])[0]
        best_guess_distances = word_to_distances[best_guess_word]
        top_distances = np.argsort(best_guess_distances)[:top]
        top_distances_mask = np.zeros(len(self.words), dtype=bool)
        top_distances_mask[top_distances] = True
        return top_distances_mask

    def already_guessed_mask(self, guesses) -> np.ndarray:
        already_guessed_mask = np.zeros(len(self.words), dtype=bool)
        for word, _ in guesses:
            word_id = self.words.index(word)
            already_guessed_mask[word_id] = True
        return already_guessed_mask

    def sample_score(self, min_gap=0.1, num_samples=500, guesses=None, word_to_distances=None) -> np.ndarray:
        if guesses is None:
            guesses = self.results

        if word_to_distances is None:
            word_to_distances = self.word_to_distances

        guesses = [(word, order)for word, order in guesses if word in word_to_distances]
        scores = self.get_score(guesses, word_to_distances, min_gap=min_gap, num_samples=num_samples)

        already_guessed_masked = self.already_guessed_mask(guesses)
        scores[already_guessed_masked] = 0

        best_scores_masked = self.best_scores(guesses, word_to_distances, top=100)
        scores[~best_scores_masked] = 0

        top_score = max(scores)

        while True:
            mask = scores >= top_score

            for word, _ in guesses:
                word_id = self.words.index(word)
                mask[word_id] = False

            closest_ids = np.arange(len(self.words))[mask]
            if len(closest_ids) > 0:
                break
            else:
                top_score -= 1

        return closest_ids

    def next_guess(self, guesses=None, word_to_distances=None) -> str:
        closest = self.sample_score(min_gap=0.3, num_samples=500, guesses=guesses, word_to_distances=word_to_distances)
        return self.words[closest[0]]
    
    def submit_word(self, word: str) -> None:
        if self.word_input is None:
            self.word_input = self.web_driver.find_element(By.CLASS_NAME, 'word')

        self.word_input.clear()
        self.word_input.send_keys(word)
        self.word_input.submit()

        sleep(self.sleep_time)
        
        try:
            response = self.web_driver.find_element(By.CLASS_NAME, 'message')
            word_score_input = response.find_element(By.CLASS_NAME, 'row')

            score = int(word_score_input.text.split('\n')[1])
            if score == WIN_SCORE:
                self.game_finished = True
            self.add_result(word, score)
        except Exception:
            pass
    
    def random_guess(self) -> str:
        return random.choice(self.words)

    def solve(self) -> None:
        sleep(self.sleep_time)
        self.submit_word(self.random_guess())

        while not self.game_finished:
            self.submit_word(self.next_guess())
