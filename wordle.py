import requests
import random
from termcolor import cprint

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"

def menu():
    print("==== WORDLE ====")
    while True:
        print("""
    1. New game
    2. Quit
""")
        choice = input().strip()

        if choice == "1":
            game()
        elif choice == "2":
            print("Bye!")
            break
        else:
            print("Unrecognized input")

def get_guess(wordlist, length=5):
    while True:
        print("""
    Enter your guess! Must be a {}-letter word
""".format(length))
        guess = input().strip().upper()
        if not guess in wordlist:
            print("Your guess is not valid")
        else:
            return guess

def game(wordlen=5):
    # TODO: save to a given location, only dl if not present
    all_words = requests.get(WORDLIST_URL).json().keys()

    words = [w.upper() for w in all_words if len(w) == wordlen]

    soln = random.sample(words,1)[0].upper()

    guesses = 0

    known = ["_" for _ in range(wordlen)]
    found = set()

    print(' '.join([c for c in known]))
    print(soln)
    while True:
        guesses += 1
        print("_________ GUESS #{} _________".format(guesses))
        guess = get_guess(words, length=wordlen)
        k2 = [None for _ in range(wordlen)]

        for i in range(len(guess)):
            gc = guess[i]
            if gc == soln[i]:
                k2[i] = gc
                cprint(gc, 'white', 'on_green', end='')
                if gc in found:
                    found.remove(gc)

            elif gc in soln:
                found.add(gc)
                cprint(gc, 'white', 'on_yellow', end='')
            else:
                print('_', end='')

            known = k2
            if guess == soln:
                print("WELL DONE! {} guess(es)".format(guesses))
                return guesses
        print('')



menu()
