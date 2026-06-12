import tkinter as tk

class StyledButton(tk.Button):
    """A modern flat button with hover states and a pointer cursor."""
    def __init__(self, parent, bg_color="#6366F1", active_bg="#4F46E5", fg_color="#FFFFFF", hover_bg="#818CF8", *args, **kwargs):
        self.normal_bg = bg_color
        self.hover_bg = hover_bg
        self.fg_color = fg_color
        
        super().__init__(
            parent,
            bg=self.normal_bg,
            fg=self.fg_color,
            activebackground=active_bg,
            activeforeground=fg_color,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            *args,
            **kwargs
        )
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _on_enter(self, event):
        if self["state"] != "disabled":
            self.config(bg=self.hover_bg)
            
    def _on_leave(self, event):
        if self["state"] != "disabled":
            self.config(bg=self.normal_bg)


class SegmentedControl(tk.Frame):
    """A horizontal segmented control where only one button is active at a time."""
    def __init__(self, parent, options, default_option=None, callback=None, bg_color="#1E1E2E", 
                 active_bg="#6366F1", active_fg="#FFFFFF", inactive_bg="#2A2A3D", inactive_fg="#A9B1D6", *args, **kwargs):
        super().__init__(parent, bg=bg_color, *args, **kwargs)
        self.options = options
        self.callback = callback
        self.active_bg = active_bg
        self.active_fg = active_fg
        self.inactive_bg = inactive_bg
        self.inactive_fg = inactive_fg
        
        self.buttons = {}
        self.selected_option = default_option or options[0]
        
        for idx, option in enumerate(options):
            # Create customized button styling
            btn = tk.Button(
                self,
                text=option,
                font=("Segoe UI", 9, "bold"),
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                command=lambda opt=option: self._select_option(opt)
            )
            btn.grid(row=0, column=idx, padx=4, pady=4, sticky="nsew")
            self.grid_columnconfigure(idx, weight=1)
            self.buttons[option] = btn
            
        self._update_styles()

    def _select_option(self, option):
        if self.selected_option == option:
            return
        self.selected_option = option
        self._update_styles()
        if self.callback:
            self.callback(option)

    def _update_styles(self):
        for option, btn in self.buttons.items():
            if option == self.selected_option:
                btn.config(bg=self.active_bg, fg=self.active_fg, activebackground=self.active_bg, activeforeground=self.active_fg)
            else:
                btn.config(bg=self.inactive_bg, fg=self.inactive_fg, activebackground=self.inactive_bg, activeforeground=self.inactive_fg)

    def set_selected(self, option):
        if option in self.buttons:
            self.selected_option = option
            self._update_styles()

    def get_selected(self):
        return self.selected_option


class CanvasProgressBar(tk.Canvas):
    """A sleek horizontal progress bar drawn on a tk.Canvas with animation support."""
    def __init__(self, parent, bg_color="#1E1E2E", bar_color="#6366F1", height=8, *args, **kwargs):
        super().__init__(parent, height=height, bg=bg_color, highlightthickness=0, borderwidth=0, *args, **kwargs)
        self.bar_color = bar_color
        self.bg_color = bg_color
        
        # State
        self.current_ratio = 1.0
        self.target_ratio = 1.0
        self.rect_id = None
        
        self.bind("<Configure>", self._on_resize)
        
    def _on_resize(self, event):
        self.redraw()
        
    def redraw(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Draw background bar (could do standard rectangle or line)
        self.create_rectangle(0, 0, width, height, fill=self.bg_color, outline="")
        
        # Draw filled bar based on current ratio
        fill_width = int(width * self.current_ratio)
        if fill_width > 0:
            self.rect_id = self.create_rectangle(0, 0, fill_width, height, fill=self.bar_color, outline="")

    def set_progress(self, ratio, animate=True):
        """Sets target progress ratio (0.0 to 1.0) and animates the transitions."""
        self.target_ratio = max(0.0, min(1.0, ratio))
        if not animate:
            self.current_ratio = self.target_ratio
            self.redraw()
        else:
            self._animate_step()

    def _animate_step(self):
        diff = self.target_ratio - self.current_ratio
        if abs(diff) < 0.02:
            self.current_ratio = self.target_ratio
            self.redraw()
        else:
            # Interpolate (15% step)
            self.current_ratio += diff * 0.15
            self.redraw()
            self.after(16, self._animate_step) # ~60fps step
