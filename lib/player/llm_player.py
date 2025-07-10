import logging
import os
import google.generativeai as genai

from lib.player.player_interface import PlayerInterface
from lib.game.game_state_interface import GameStateInterface

class LLMPlayer(PlayerInterface):
    """
    A player that uses the Gemini LLM to generate a word guess.
    """

    def __init__(self, game_state, words=None, word_scorer=None):
        self.placed = ['' for _ in range(game_state.word_length)]
        self.present = set()
        self.guessed = set()
        self.filter = set()
        self.excludes = [set() for _ in range(game_state.word_length)]
        
        # Configure the Gemini API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel('gemini-2.0-flash')


    def guess(self, game_state, prev=None) -> str:
        placed_str = ''.join(self.placed)
        if len(placed_str) == game_state.word_length:
            return placed_str

        guess = self._generate_guess(game_state)

        if not guess:
            raise Exception("Guess generation failed!")
        else:
            self.guessed.add(guess)
            logging.info(f"LLM guessed: {guess}")
            return guess

    def update_state(self, result) -> None:
        letters = result.letters
        guess = result.guess
        seen = set()
        for i, pair in enumerate(letters):
            if not pair:
                if not guess[i] in seen: self.filter.add(guess[i])
                continue
            l, l_state = pair
            if l_state == GameStateInterface.LETTER_STATE_PRESENT:
                self.excludes[i].add(l)
                self.present.add(l)
                self.filter.discard(l)
            elif l_state == GameStateInterface.LETTER_STATE_PLACED:
                self.placed[i] = l
                # TODO: how do we account for the possibility
                # that a placed letter occurs again?
                self.filter.discard(l)
                self.present.discard(l)
            seen.add(guess[i])

    def _generate_guess(self, game_state):
        prompt = self._generate_prompt(game_state)
        logging.debug(f"Prompt: {prompt}")
        try:
            logging.info("Generating guess with Gemini...")
            response = self.llm.generate_content(prompt)
            guess = response.text.strip().upper()
            # Basic validation
            if len(guess) == game_state.word_length and guess.isalpha():
                return guess
            else:
                logging.error(f"LLM returned invalid guess: '{guess}'")
                return None
        except Exception as e:
            logging.error(f"Error calling Gemini API: {e}")
            return None

    def _generate_prompt(self, game_state, prev=None) -> str:
        placed_str = ''.join([l if l else '?' for l in self.placed])
        absent_str = ', '.join(sorted(list(self.filter)))
        present_str = ', '.join(sorted(list(self.present)))
        excluded_str = self._generate_excludes_str()

        prompt = f"""
WORDLE CONSTRAINT SOLVER - {game_state.word_length} letters

## FIXED PATTERN: {placed_str}
## MUST INCLUDE (different positions): {present_str}
## FORBIDDEN LETTERS: {absent_str}
## POSITION BLOCKS: {excluded_str}

INSTRUCTION: Complete the pattern {placed_str} by filling in the ? positions.

RULES:
1. Letters marked as specific letters (not ?) cannot be changed
2. Include all present letters in different positions than where they were found
3. Never use forbidden letters
4. Result must be a real English word

PROCESS:
- Take the pattern: {placed_str}
- Replace each ? with a valid letter
- Verify all constraints satisfied
- Choose the most common English word that fits

OUTPUT: Complete {game_state.word_length}-letter word in UPPERCASE only.
    NEVER INCLUDE ANY OTHER TEXT OR EXPLANATION.
"""

        return prompt

    def _generate_excludes_str(self):
        excludes_str = ""
        for i, letters in enumerate(self.excludes):
            if letters:
                excludes_str += f"  - Position {i+1} cannot be: {', '.join(sorted(list(letters)))}\n"
        return excludes_str if excludes_str else "  - None\n"
