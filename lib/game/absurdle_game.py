import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from pyshadow.main import Shadow
from tkinter import Tk

from lib.game.game_interface import GameInterface
from lib.game.game_guess_result import GameGuessResult

class AbsurdleGame(GameInterface):
    GAME_URL = "https://qntm.org/files/wordle/index.html"

    def __init__(self, headless=True):
        self.guesses = 0
        self.word_length = 5
        self.max_guesses = None
        self.headless = headless
        
        self.browser = self._init_browser()

    def update(self, guess):
        for letter in guess.upper(): self._press_key(letter)
        self._press_key("enter")
        time.sleep(1)

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

        return browser

    def _find_element_by_text(self, selector, text):
        els = self.browser.find_elements(selector)
        try:
            match = next(e for e in els if e.text == text)
            return match
        except StopIteration:
            return None

    def _press_key(self, text):
        selector = 'button.absurdle__button'
        key_el = self._find_element_by_text(selector, text)
        if key_el:
            key_el.click()
            return True
        else:
            return False

    def _clear_row(self):
        # TODO: the text value of the backspace key changes
        # handle cases where we can't find based on text
        [self._press_key("⌫") for _ in range(5)]

    def _get_result(self):
        if self._find_element_by_text(
                'absurdle__button--primary',
                'not a word'
        ):
            return None

        rows = self.browser.find_elements(
            'table.absurdle__guess-table>tr'
        )
        current_row = rows[-2]
        tiles = self.browser.find_elements(current_row, 'td.absurdle__guess-box')

        letter_results = []
        for tile in tiles:
            classes = tile.get_attribute('class').split()
            letter = tile.text.upper()
            res = None
            if 'absurdle__guess-box--exact' in classes:
                res = (letter, self.LETTER_STATE_PLACED)
            elif 'absurdle__guess-box--inexact' in classes:
                res = (letter, self.LETTER_STATE_PRESENT)
            elif 'absurdle__guess-box--wrong' in classes:
                res = None
            else:
                # TODO: better logging, ofc
                print(f'Unsupported evaluation: {classes}')
                return None

            letter_results.append(res)

        share_btn = self._get_share_btn()
        guess_correct = not not share_btn
        res_text = self._get_result_text(share_btn) if guess_correct else None

        result = GameGuessResult(
            ''.join([t.text for t in tiles]),
            letters=letter_results,
            correct=guess_correct,
            text=res_text
        )
        return result

    def _get_share_btn(self):
        btn_text = 'copy replay to clipboard'
        return self._find_element_by_text('button', btn_text)

    def _get_result_text(self, share_btn):
        share_btn.click()
        result_str = Tk().clipboard_get()
        return result_str
