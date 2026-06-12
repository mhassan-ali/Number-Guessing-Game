import tkinter as tk
from game import NumberGuessingGame, DIFFICULTY_LEVELS
from .components import StyledButton, SegmentedControl, CanvasProgressBar

class NumberGuessingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Number Guessing Game")
        self.width = 460
        self.height = 580
        self.center_window()
        self.resizable(False, False)
        
        # Color Palette Design Tokens
        self.colors = {
            "bg_main": "#1E1E2E",         # Dark theme background
            "bg_card": "#252538",         # Secondary container card
            "text_primary": "#FFFFFF",     # Primary text color
            "text_muted": "#A9B1D6",       # Muted text color
            "accent": "#6366F1",           # Indigo accent color
            "accent_hover": "#818CF8",     # Indigo hover highlight
            
            # Status colors
            "status_start_bg": "#1E1E2E",
            "status_start_fg": "#A9B1D6",
            "status_correct_bg": "#064E3B",
            "status_correct_fg": "#34D399",
            "status_fail_bg": "#7F1D1D",
            "status_fail_fg": "#F87171",
            "status_hint_bg": "#31314B",
            "status_hint_fg": "#F59E0B"
        }
        
        self.configure(bg=self.colors["bg_main"])
        
        # Game logic setup
        self.game = NumberGuessingGame()
        
        # Timer tracking state
        self.timer_scheduled = False
        
        # Build layout
        self.create_widgets()
        
        # Initialize first game
        self.start_new_game()

    def center_window(self):
        """Centers the Tkinter window on the screen."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def create_widgets(self):
        # Outer Padding Container
        self.main_container = tk.Frame(self, bg=self.colors["bg_main"], padx=25, pady=25)
        self.main_container.pack(fill="both", expand=True)
        
        # --- HEADER SECTION ---
        self.header_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.header_frame.pack(fill="x", pady=(0, 15))
        
        self.title_label = tk.Label(
            self.header_frame, 
            text="NUMBER GUESSER", 
            font=("Segoe UI", 24, "bold"), 
            fg=self.colors["text_primary"], 
            bg=self.colors["bg_main"]
        )
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(
            self.header_frame, 
            text="Decipher the hidden value before attempts run dry.", 
            font=("Segoe UI", 9), 
            fg=self.colors["text_muted"], 
            bg=self.colors["bg_main"]
        )
        self.subtitle_label.pack(pady=(2, 0))
        
        # --- CARD SECTION ---
        self.card_frame = tk.Frame(
            self.main_container, 
            bg=self.colors["bg_card"], 
            padx=20, 
            pady=20
        )
        self.card_frame.pack(fill="both", expand=True)
        
        # 1. Difficulty Segment
        self.diff_title = tk.Label(
            self.card_frame, 
            text="DIFFICULTY LEVEL", 
            font=("Segoe UI", 8, "bold"), 
            fg=self.colors["text_muted"], 
            bg=self.colors["bg_card"]
        )
        self.diff_title.pack(anchor="w")
        
        self.difficulty_control = SegmentedControl(
            self.card_frame, 
            options=["Easy", "Medium", "Hard"],
            default_option="Easy",
            callback=self.change_difficulty,
            bg_color=self.colors["bg_card"],
            active_bg=self.colors["accent"],
            active_fg=self.colors["text_primary"],
            inactive_bg=self.colors["bg_main"],
            inactive_fg=self.colors["text_muted"]
        )
        self.difficulty_control.pack(fill="x", pady=(5, 15))
        
        # 2. Stats Grid
        self.stats_frame = tk.Frame(self.card_frame, bg=self.colors["bg_card"])
        self.stats_frame.pack(fill="x", pady=(0, 15))
        
        self.range_label = tk.Label(
            self.stats_frame, 
            text="Range: 1 - 50", 
            font=("Segoe UI", 10, "bold"), 
            fg=self.colors["text_primary"], 
            bg=self.colors["bg_card"]
        )
        self.range_label.pack(side="left")
        
        self.best_score_label = tk.Label(
            self.stats_frame, 
            text="Personal Best: --", 
            font=("Segoe UI", 9, "italic"), 
            fg=self.colors["text_muted"], 
            bg=self.colors["bg_card"]
        )
        self.best_score_label.pack(side="right")
        
        # 3. Attempts & Timer Status
        self.progress_status_frame = tk.Frame(self.card_frame, bg=self.colors["bg_card"])
        self.progress_status_frame.pack(fill="x", pady=(5, 2))
        
        self.attempts_label = tk.Label(
            self.progress_status_frame, 
            text="Attempts remaining: 10/10", 
            font=("Segoe UI", 9), 
            fg=self.colors["text_muted"], 
            bg=self.colors["bg_card"]
        )
        self.attempts_label.pack(side="left")
        
        self.timer_label = tk.Label(
            self.progress_status_frame, 
            text="Time: 0.0s", 
            font=("Segoe UI", 9, "bold"), 
            fg=self.colors["accent"], 
            bg=self.colors["bg_card"]
        )
        self.timer_label.pack(side="right")
        
        # 4. Animated Custom Progress Bar
        self.progress_bar = CanvasProgressBar(
            self.card_frame, 
            bg_color=self.colors["bg_main"], 
            bar_color=self.colors["accent"], 
            height=6
        )
        self.progress_bar.pack(fill="x", pady=(2, 20))
        
        # 5. Entry & Submit Input Panel
        self.input_frame = tk.Frame(self.card_frame, bg=self.colors["bg_card"])
        self.input_frame.pack(fill="x", pady=(0, 15))
        self.input_frame.grid_columnconfigure(0, weight=3)
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        self.guess_entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 14, "bold"),
            justify="center",
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"],
            insertbackground="white",      # White blinking text cursor
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#313143",
            highlightcolor=self.colors["accent"]
        )
        self.guess_entry.grid(row=0, column=0, sticky="nsew", ipady=8)
        self.guess_entry.bind("<Return>", lambda event: self.submit_guess())
        
        self.submit_btn = StyledButton(
            self.input_frame,
            text="GUESS",
            font=("Segoe UI", 10, "bold"),
            bg_color=self.colors["accent"],
            active_bg=self.colors["accent_hover"],
            hover_bg=self.colors["accent_hover"],
            fg_color=self.colors["text_primary"],
            command=self.submit_guess
        )
        self.submit_btn.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # 6. Large Feedback Banner
        self.feedback_container = tk.Frame(
            self.card_frame, 
            bg=self.colors["status_start_bg"], 
            padx=10, 
            pady=10
        )
        self.feedback_container.pack(fill="both", expand=True, pady=(0, 15))
        self.feedback_container.pack_propagate(False) # Prevent card resizing dynamically
        
        self.feedback_label = tk.Label(
            self.feedback_container,
            text="Pick a difficulty and input a guess to start the search!",
            font=("Segoe UI", 10),
            fg=self.colors["status_start_fg"],
            bg=self.colors["status_start_bg"],
            wraplength=340,
            justify="center"
        )
        self.feedback_label.pack(fill="both", expand=True)
        
        # 7. Action Control Footer
        self.restart_btn = StyledButton(
            self.card_frame,
            text="RESTART GAME",
            font=("Segoe UI", 9, "bold"),
            bg_color="#374151",
            active_bg="#4B5563",
            hover_bg="#4B5563",
            fg_color=self.colors["text_primary"],
            command=self.start_new_game
        )
        self.restart_btn.pack(fill="x", ipady=6)

    def start_new_game(self):
        """Initializes game state, clears input fields, and starts the timer."""
        difficulty = self.difficulty_control.get_selected()
        self.game.start_game(difficulty)
        
        # Clean widgets
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()
        self.submit_btn.config(state="normal")
        
        # Reset labels
        self.range_label.config(text=f"Range: 1 - {self.game.max_val}")
        self.update_attempts_display()
        self.update_best_score_display()
        self.timer_label.config(text="Time: 0.0s")
        
        # Reset progress bar
        self.progress_bar.set_progress(1.0, animate=False)
        
        # Reset feedback
        self.update_feedback("start", f"I'm thinking of a number between 1 and {self.game.max_val}.\nEnter your guess above!")
        
        # Reset and trigger timer loop
        if not self.timer_scheduled:
            self.timer_scheduled = True
            self.update_timer()

    def change_difficulty(self, difficulty):
        """Callback for SegmentedControl selection."""
        self.start_new_game()

    def submit_guess(self):
        """Validates input, processes a guess, and transitions state."""
        if self.game.game_over:
            return
            
        raw_val = self.guess_entry.get()
        
        # 1. Validation Step
        try:
            val = self.game.validate_guess(raw_val)
        except ValueError as err:
            self.update_feedback("error", str(err))
            self.shake_window()
            return

        # 2. State update
        status, msg = self.game.make_guess(val)
        
        # 3. Clean entry
        self.guess_entry.delete(0, tk.END)
        
        # 4. GUI presentation
        self.update_attempts_display()
        self.progress_bar.set_progress(self.game.get_remaining_turns() / self.game.total_turns)
        
        if status == 'correct':
            self.update_feedback("correct", msg)
            self.guess_entry.config(state="disabled")
            self.submit_btn.config(state="disabled")
            self.update_best_score_display()
        elif status == 'game_over':
            self.update_feedback("fail", msg)
            self.guess_entry.config(state="disabled")
            self.submit_btn.config(state="disabled")
        elif status in ['low', 'high']:
            self.update_feedback("hint", msg)

    def update_attempts_display(self):
        rem = self.game.get_remaining_turns()
        tot = self.game.total_turns
        self.attempts_label.config(text=f"Attempts remaining: {rem}/{tot}")

    def update_best_score_display(self):
        best = self.game.best_turns[self.game.difficulty]
        best_str = f"{best} attempts" if best is not None else "--"
        self.best_score_label.config(text=f"Personal Best: {best_str}")

    def update_feedback(self, status, text):
        """Helper to style the central notification banner according to state."""
        bg_key = f"status_{status}_bg"
        fg_key = f"status_{status}_fg"
        
        bg_color = self.colors.get(bg_key, self.colors["bg_main"])
        fg_color = self.colors.get(fg_key, self.colors["text_primary"])
        
        self.feedback_container.config(bg=bg_color)
        self.feedback_label.config(bg=bg_color, fg=fg_color, text=text)

    def update_timer(self):
        """Live ticks timer representation on screen."""
        if not self.game.game_over and self.game.start_time is not None:
            elapsed = self.game.get_elapsed_time()
            self.timer_label.config(text=f"Time: {elapsed:.1f}s")
            self.after(100, self.update_timer)
        else:
            self.timer_scheduled = False
            # Render final static time if finished
            if self.game.elapsed_time is not None:
                self.timer_label.config(text=f"Time: {self.game.elapsed_time:.1f}s")

    def shake_window(self):
        """Shakes the application window window horizontally on invalid interaction."""
        try:
            orig_geom = self.geometry()
            parts = orig_geom.split('+')
            if len(parts) == 3:
                w_h = parts[0]
                orig_x = int(parts[1])
                orig_y = int(parts[2])
                
                # Perform back-and-forth movement offsets
                for offset in [8, -8, 6, -6, 4, -4, 2, -2, 0]:
                    self.geometry(f"{w_h}+{orig_x + offset}+{orig_y}")
                    self.update()
                    self.after(15)
        except Exception:
            pass  # Fail-safe in case window is closed during animation
