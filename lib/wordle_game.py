import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
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
        driver.set_page_load_timeout(10)

        browser = Shadow(driver)

        browser.driver.get(self.GAME_URL)
        time.sleep(1)

        browser.find_element('button#pz-gdpr-btn-closex').click()
        browser.find_element('game-app').click()
        return browser

    def _press_key(self, letter):
        keyboard = self.browser.find_element('#keyboard')
        key_el = keyboard.find_element('css selector', f'button[data-key="{letter.lower()}"]')
        # TODO: why are clicks spamming 'QA--QAQA True'?
        key_el.click()

    def _clear_row(self):
        for _ in range(5): self._press_key("←")

    def _get_result(self):
        rows = self.browser.find_elements('game-row')
        current_row = [r for r in rows if r.get_attribute('letters')][-1]
        tiles = self.browser.find_elements(current_row, 'game-tile')

        letter_results = []
        for tile in tiles:
            evaluation = tile.get_attribute('evaluation')
            letter = tile.get_attribute('letter').upper()
            res = None
            if evaluation == 'correct':
                res = (letter, self.LETTER_STATE_PLACED)
            elif evaluation == 'present':
                res = (letter, self.LETTER_STATE_PRESENT)
            elif evaluation == 'absent':
                res = None
            else:
                # TODO: better logging, ofc
                print(f'Unsupported evaluation: {evaluation}')
                return None

            letter_results.append(res)

        share_btn = self._get_share_btn()
        game_over = not not share_btn
        game_won = not self._game_lost()
        guess_correct = game_over and game_won

        res_text = self._get_result_text(share_btn) if game_over else None

        result = GameGuessResult(
            current_row.get_attribute('letters'),
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
        except NoSuchElementException:
            return False

    def _get_share_btn(self):
        try:
            btn = self.browser.find_element('button#share-button')
            return btn
        except NoSuchElementException:
            return None

    def _get_result_text(self, share_btn):
        share_btn.click()
        result_str = Tk().clipboard_get()
        return result_str
