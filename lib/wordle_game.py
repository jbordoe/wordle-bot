import logging
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from pyshadow.main import Shadow
from tkinter import Tk

from lib.game_guess_result import GameGuessResult
from lib.game_state_interface import GameStateInterface

class WordleGame(GameStateInterface):
    GAME_URL = "https://www.nytimes.com/games/wordle/index.html"

    def __init__(self, headless=True):
        self.guesses = 0
        self.word_length = 5
        self.max_guesses = 6
        self.headless = headless
        self.browser = self._init_browser()

    def update(self, guess):
        for letter in guess: self._press_key(letter)
        self._press_key("↵")
        time.sleep(5)

        result = self._get_result()

        if not result:
            self._clear_row()

        return result

    def quit(self):
        self.browser.driver.quit()

    def _init_browser(self):
        options = Options()
        options.headless = self.headless

        driver = webdriver.Firefox(options=options)
        driver.set_page_load_timeout(15)

        browser = Shadow(driver)
        self.browser = browser

        browser.driver.get(self.GAME_URL)

        self._handle_cookie_dialog()
        self._begin_game()


        return browser

    def _begin_game(self):
        try:
            button = WebDriverWait(self.browser.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Play')]")
                )
            )
            button.click()
        except (TimeoutException, NoSuchElementException) as e:
            raise Exception('Game initialization failed: ' + str(e))

        try:
            close_modal = WebDriverWait(self.browser.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f'//button[contains(@class, "Modal-module_closeIcon__")]')
                )
            )
            close_modal.click()
        except (TimeoutException, NoSuchElementException) as e:
            raise Exception('Game initialization failed: ' + str(e))

    def _handle_cookie_dialog(self):
        try:
            WebDriverWait(self.browser.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'fides-overlay'))
            )
            self.browser.driver.execute_script(
                "arguments[0].remove();",
                self.browser.driver.find_element('id', 'fides-overlay')
            )
        except TimeoutException:
            logging.warning("Cookie dialog did not appear")
        except NoSuchElementException:
            logging.warning("div.fides-overlay not found")
        except Exception as e:
            logging.warning(f"An error occurred while handling cookie dialog: {e}")

    def _press_key(self, letter):
        keyboard = self._find_el_by_class_substr('Keyboard-module_keyboard')
        key_el = keyboard.find_element('css selector', f'button[data-key="{letter.lower()}"]')
        # TODO: why are clicks spamming 'QA--QAQA True'?
        key_el.click()

    def _clear_row(self):
        for _ in range(5): self._press_key("←")

    def _get_result(self):
        tiles = self._get_last_row()

        letter_results = []
        for tile in tiles:
            evaluation = tile.get_attribute('data-state')
            letter = tile.text.upper()
            res = None
            if evaluation == 'correct':
                res = (letter, self.LETTER_STATE_PLACED)
            elif evaluation == 'present':
                res = (letter, self.LETTER_STATE_PRESENT)
            elif evaluation == 'absent':
                res = None
            else:
                logging.error(f'Unsupported evaluation: {evaluation}')
                return None

            letter_results.append(res)

        share_btn = self._get_share_btn()
        game_over = not not share_btn
        game_won = not self._game_lost()
        guess_correct = game_over and game_won

        res_text = self._get_result_text(share_btn) if game_over else None

        result = GameGuessResult(
            [t.text.upper() for t in tiles],
            letters=letter_results,
            correct=guess_correct,
            text=res_text
        )
        return result

    def _game_lost(self):
        try:
            self.browser.find_element(
                'div#game-toaster[duration="infinity"]'
            )
            return True
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def _get_share_btn(self):
        try:
            btn = self.browser.find_element('button#share-button')
            return btn
        except (NoSuchElementException, ElementNotVisibleException):
            return None

    def _get_result_text(self, share_btn):
        share_btn.click()
        result_str = Tk().clipboard_get()
        return result_str

    def _get_last_row(self):
        tiles = self._find_els_by_class_substr('Tile-module_tile')
        rows = [tiles[i:i+5] for i in range(0, len(tiles), 5)]

        valid_states = ['present', 'absent', 'correct']
        return [r for r in rows if all(t.get_attribute('data-state') in valid_states for t in r)][-1]

    def _find_els_by_class_substr(self, substr, tag='*'):
        return self.browser.driver.find_elements(
            by=By.XPATH,
            value=f'//{tag}[contains(@class, "{substr}")]'
        )
    def _find_el_by_class_substr(self, substr, tag='*'):
        els = self._find_els_by_class_substr(substr, tag=tag)
        return els[0] if els else None

