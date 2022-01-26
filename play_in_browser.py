import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from pyshadow.main import Shadow
from tkinter import Tk

from lib.player.naive_player import NaivePlayer
from lib.game_state import GameState
from lib.words.word_index import WordIndex
from lib.game_guess_result import GameGuessResult

WORDLIST_PATH = "dict.json"

def load_words(wordlen=5):
    print("loading wordlist...")
    all_words = json.load(open(WORDLIST_PATH)).keys()
    word_list = []
    for w in all_words:
        if len(w) != wordlen or set(" -").intersection(set(w)):
            continue
        w = w.upper()
        word_list.append(w)
    return word_list

def init_browser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.set_page_load_timeout(10)
    
    shadow = Shadow(driver)
    
    return shadow

def press_key(browser, letter):
    keyboard = browser.find_element('#keyboard')
    key_el = keyboard.find_element('css selector', f'button[data-key="{letter.lower()}"]')
    key_el.click()

def get_result(browser):
    rows = browser.find_elements('game-row')
    current_row = [r for r in rows if r.get_attribute('letters')][-1]
    tiles = browser.find_elements(current_row, 'game-tile')

    letter_results = []
    for tile in tiles:
        evaluation = tile.get_attribute('evaluation')
        letter = tile.get_attribute('letter')
        res = None
        if evaluation == 'correct':
            res = (letter, GameState.LETTER_STATE_PLACED)
        elif evaluation == 'present':
            res = (letter, GameState.LETTER_STATE_PRESENT)
        elif evaluation == 'absent':
            res = None
        else:
            # TODO: better logging, ofc
            print(f'Unsupported evaluation: {evaluation}')
            return None
    
        letter_results.append(res)

    return GameGuessResult(current_row.get_attribute('letters'), letters=letter_results)

def game_won(browser):
    try:
        btn = browser.find_element('button#share-button')
        return btn
    except NoSuchElementException:
        return None

def init_player(state):
    words = load_words()
    word_index = WordIndex(words)
    player = NaivePlayer(state, words=word_index)
    return player

def go():
    browser = init_browser() 

    url = "https://www.powerlanguage.co.uk/wordle/"

    print("Visiting wordle site")
    browser.driver.get(url)
    time.sleep(1)    

    root = browser.find_element('game-app')
    root.click()

    # TODO: we shouldn't need this object here...
    state = GameState(["hello"], wordlen=5)
    player = init_player(state)

    result = None
    guesses = 0 
    guessed = set()

    while True:
        print('Selecting a word...')
        guess = player.guess(state, prev=result)

        if not guess:
            print(result.letters)
            raise Exception("Could not find a word!")

        print(f'Guess #{guesses+1} is {guess}')
        player.guessed.add(guess)

        for letter in guess:
            press_key(browser, letter)

        press_key(browser, "↵")
        time.sleep(5)

        print("Checking results...")
        result = get_result(browser)

        if not result:
            print("Guess was invalid, trying something else")
            [press_key(browser, "←") for _ in range(5)]
        else:
            guesses += 1
            win_btn = game_won(browser)
            if win_btn:
                print("Wordle found!")
                win_btn.click()
                r = Tk()
                game_str = r.clipboard_get()
                print(game_str)
                print("Closing browser in 30 seconds")
                time.sleep(30)
                break
            else:
                print("Updating...")
                player.update_state(result)

        if guesses == 6:
            print("Could not find the Wordle!")
            break

    browser.driver.quit()
go()
