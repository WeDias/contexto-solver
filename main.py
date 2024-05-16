from selenium import webdriver

from src.solver import Solver
from src.config import CONTEXTO_URL


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    options.add_experimental_option("detach", True)

    web_driver = webdriver.Chrome(options=options)
    web_driver.get(CONTEXTO_URL)

    solver = Solver(web_driver=web_driver, sleep_time=2, random_guesses=5)
    solver.solve()
