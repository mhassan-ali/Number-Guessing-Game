import random
import time

DIFFICULTY_LEVELS = {
    'Easy': (50, 10),     # (max_value, total_turns)
    'Medium': (100, 7),
    'Hard': (200, 5)
}

class NumberGuessingGame:
    def __init__(self):
        self.difficulty = 'Easy'
        self.max_val, self.total_turns = DIFFICULTY_LEVELS[self.difficulty]
        self.secret_number = None
        self.turns_used = 0
        self.start_time = None
        self.elapsed_time = None
        self.game_over = False
        self.won = False
        self.best_turns = {level: None for level in DIFFICULTY_LEVELS}

    def start_game(self, difficulty: str = 'Easy') -> None:
        """Starts a new game with the specified difficulty."""
        if difficulty not in DIFFICULTY_LEVELS:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        
        self.difficulty = difficulty
        self.max_val, self.total_turns = DIFFICULTY_LEVELS[self.difficulty]
        self.secret_number = random.randint(1, self.max_val)
        self.turns_used = 0
        self.start_time = time.time()
        self.elapsed_time = None
        self.game_over = False
        self.won = False

    def validate_guess(self, guess_str: str) -> int:
        """Validates that a guess string is a valid integer within the active range."""
        cleaned_str = guess_str.strip()
        if not cleaned_str:
            raise ValueError("Guess input cannot be empty.")
        
        if not cleaned_str.isdigit():
            # Support negative numbers checks specifically or reject non-digits
            if cleaned_str.startswith('-') and cleaned_str[1:].isdigit():
                raise ValueError(f"Please enter a positive number between 1 and {self.max_val}.")
            raise ValueError("Please enter a valid positive whole number.")
            
        val = int(cleaned_str)
        if val < 1 or val > self.max_val:
            raise ValueError(f"Guess out of bounds! Choose between 1 and {self.max_val}.")
        
        return val

    def make_guess(self, guess: int) -> tuple[str, str]:
        """Processes a validated guess, updates game state, and returns (status, message)."""
        if self.game_over:
            return 'error', 'The game is already over. Start a new game.'
            
        if guess < 1 or guess > self.max_val:
            raise ValueError(f"Guess must be between 1 and {self.max_val}.")

        self.turns_used += 1

        if guess == self.secret_number:
            self.won = True
            self.game_over = True
            self.elapsed_time = round(time.time() - self.start_time, 2)
            
            # Update best score (lowest turns) for this difficulty
            current_best = self.best_turns[self.difficulty]
            if current_best is None or self.turns_used < current_best:
                self.best_turns[self.difficulty] = self.turns_used
            
            return 'correct', f"🎉 Correct! You guessed it in {self.turns_used} attempts!\nSolve time: {self.elapsed_time} seconds."

        if self.turns_used >= self.total_turns:
            self.game_over = True
            self.elapsed_time = round(time.time() - self.start_time, 2)
            return 'game_over', f"😢 Game Over! Out of attempts.\nThe number was: {self.secret_number}"

        if guess < self.secret_number:
            return 'low', "⬆️ Too Low! Try guessing a higher number."
        else:
            return 'high', "⬇️ Too High! Try guessing a lower number."

    def get_remaining_turns(self) -> int:
        """Returns the number of turns remaining in the active game."""
        return max(0, self.total_turns - self.turns_used)

    def get_elapsed_time(self) -> float:
        """Returns elapsed time in seconds. Dynamic if game is in progress."""
        if self.game_over:
            return self.elapsed_time if self.elapsed_time is not None else 0.0
        if self.start_time is None:
            return 0.0
        return round(time.time() - self.start_time, 1)
