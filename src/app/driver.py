from time import sleep

from constants import (GRID_CELL_ID, PUZZLE_IFRAME_CSS, QUEENS_GRID_ID,
                       SOLVE_PUZZLE_BUTTON_ID, SOURCE_TO_URL_MAP)
from helpers import index_to_coordinate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChromeDriver:
    def __init__(self, source: str):
        self.options = Options()
        self.source = source
        #self.options.add_argument("--start-fullscreen")

        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
            poll_frequency=0.1
        )
    
    def fetch_queens_grid_html(self):
        func_map = {
            'Queens Game': self.__fetch_queens_game_grid,
            'Linkedin Queens': self.__fetch_linkedin_queens_grid
        }
        return func_map[self.source](url=SOURCE_TO_URL_MAP[self.source])


    def put_solution_to_grid(self, solution: list):
        try:
            func_map = {
                'Queens Game': self.__put_solution_queens_game,
                'Linkedin Queens': self.__put_solution_linkedin_queens
            }
            func_map[self.source](solution=solution)
        except Exception as e:
            self.driver.close()
    

    def __fetch_linkedin_queens_grid(self, url: str) -> str:
        self.driver.get(url)
        
        puzzle_iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, PUZZLE_IFRAME_CSS)))
        self.driver.switch_to.frame(puzzle_iframe)

        start_button = self.wait.until(EC.presence_of_element_located((By.ID, SOLVE_PUZZLE_BUTTON_ID)))
        start_button.click()

        queens_grid = self.wait.until(EC.presence_of_element_located((By.ID, QUEENS_GRID_ID)))
        return queens_grid.get_attribute('outerHTML')
    

    def __fetch_queens_game_grid(self, url: str) -> str:
        self.driver.get(url)
        sleep(3)

        queens_grid = self.wait.until(EC.presence_of_element_located((By.ID, 'grid')))
        return queens_grid.get_attribute('outerHTML')
    

    def __put_solution_linkedin_queens(self, solution: list):
        # Close Popup (If Exists)
        try:
            popup_close = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Dismiss"]'))
            )
            popup_close.click()
        except:
            pass

        solution_indexes, _ = solution

        for index in solution_indexes:
            div = self.driver.find_elements(By.CSS_SELECTOR, GRID_CELL_ID.format(index=index))
            div[0].click()
            div[0].click()
        
        sleep(5)


    def __put_solution_queens_game(self, solution: tuple):
        _, solution_coordinates = solution

        for r, c in solution_coordinates:
            cell = self.wait.until(EC.presence_of_element_located((By.ID, f"case-{r}-{c}")))
            cell.click()
        
        sleep(5)
