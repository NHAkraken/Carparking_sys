import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime


class ClockApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Clock, Stopwatch & Timer")
        self.root.geometry("420x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Stopwatch state
        self.sw_running = False
        self.sw_start_time = 0.0
        self.sw_elapsed = 0.0

        # Timer state
        self.tm_running = False
        self.tm_remaining = 0

        self._build_ui()
        self._update_clock()

    def _build_ui(self):
        # Navigation Tabs
        nav_frame = tk.Frame(self.root, bg="#181825")
        nav_frame.pack(fill="x")

        btn_style = {
            "bg": "#181825",
            "fg": "#cdd6f4",
            "activebackground": "#313244",
            "activeforeground": "#ffffff",
            "bd": 0,
            "font": ("Segoe UI", 11, "bold"),
            "pady": 10,
            "cursor": "hand2",
        }

        tk.Button(nav_frame, text="Clock", command=lambda: self.show_frame("clock"), **btn_style).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="Stopwatch", command=lambda: self.show_frame("stopwatch"), **btn_style).pack(side="left", expand=True, fill="x")
        tk.Button(nav_frame, text="Timer", command=lambda: self.show_frame("timer"), **btn_style).pack(side="left", expand=True, fill="x")

        # Container for views
        self.container = tk.Frame(self.root, bg="#1e1e2e")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.frames = {}
        self._create_clock_frame()
        self._create_stopwatch_frame()
        self._create_timer_frame()

        self.show_frame("clock")

    def show_frame(self, name: str):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(expand=True, fill="both")

    # ---------------- 1. DIGITAL CLOCK ----------------
    def _create_clock_frame(self):
        frame = tk.Frame(self.container, bg="#1e1e2e")
        self.frames["clock"] = frame

        self.time_label = tk.Label(frame, font=("Consolas", 42, "bold"), bg="#1e1e2e", fg="#89b4fa")
        self.time_label.pack(pady=(35, 5))

        self.date_label = tk.Label(frame, font=("Segoe UI", 13), bg="#1e1e2e", fg="#a6adc8")
        self.date_label.pack()

    def _update_clock(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%A, %B %d, %Y"))
        self.root.after(200, self._update_clock)

    # ---------------- 2. STOPWATCH ----------------
    def _create_stopwatch_frame(self):
        frame = tk.Frame(self.container, bg="#1e1e2e")
        self.frames["stopwatch"] = frame

        self.sw_label = tk.Label(frame, text="00:00:00.00", font=("Consolas", 34, "bold"), bg="#1e1e2e", fg="#a6e3a1")
        self.sw_label.pack(pady=(25, 25))

        btn_box = tk.Frame(frame, bg="#1e1e2e")
        btn_box.pack()

        self.sw_start_btn = tk.Button(btn_box, text="Start", width=9, command=self._toggle_stopwatch, bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 10, "bold"), bd=0, pady=6, cursor="hand2")
        self.sw_start_btn.grid(row=0, column=0, padx=6)

        tk.Button(btn_box, text="Reset", width=9, command=self._reset_stopwatch, bg="#f38ba8", fg="#11111b", font=("Segoe UI", 10, "bold"), bd=0, pady=6, cursor="hand2").grid(row=0, column=1, padx=6)

    def _toggle_stopwatch(self):
        if not self.sw_running:
            self.sw_running = True
            self.sw_start_time = time.perf_counter() - self.sw_elapsed
            self.sw_start_btn.config(text="Pause", bg="#f9e2af")
            self._update_stopwatch()
        else:
            self.sw_running = False
            self.sw_start_btn.config(text="Resume", bg="#a6e3a1")

    def _reset_stopwatch(self):
        self.sw_running = False
        self.sw_elapsed = 0.0
        self.sw_label.config(text="00:00:00.00")
        self.sw_start_btn.config(text="Start", bg="#a6e3a1")

    def _update_stopwatch(self):
        if self.sw_running:
            self.sw_elapsed = time.perf_counter() - self.sw_start_time
            mins, secs = divmod(self.sw_elapsed, 60)
            hours, mins = divmod(mins, 60)
            centiseconds = int((self.sw_elapsed - int(self.sw_elapsed)) * 100)
            self.sw_label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}.{centiseconds:02d}")
            self.root.after(20, self._update_stopwatch)

    # ---------------- 3. COUNTDOWN TIMER ----------------
    def _create_timer_frame(self):
        frame = tk.Frame(self.container, bg="#1e1e2e")
        self.frames["timer"] = frame

        self.tm_label = tk.Label(frame, text="00:00:00", font=("Consolas", 36, "bold"), bg="#1e1e2e", fg="#fab387")
        self.tm_label.pack(pady=(10, 10))

        # Time input fields
        input_box = tk.Frame(frame, bg="#1e1e2e")
        input_box.pack(pady=(0, 15))

        self.hr_var = tk.StringVar(value="00")
        self.min_var = tk.StringVar(value="05")
        self.sec_var = tk.StringVar(value="00")

        entry_style = {"width": 4, "font": ("Consolas", 14), "justify": "center", "bg": "#313244", "fg": "#ffffff", "bd": 0, "insertbackground": "white"}

        tk.Entry(input_box, textvariable=self.hr_var, **entry_style).grid(row=0, column=0, padx=4)
        tk.Label(input_box, text=":", bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 14)).grid(row=0, column=1)
        tk.Entry(input_box, textvariable=self.min_var, **entry_style).grid(row=0, column=2, padx=4)
        tk.Label(input_box, text=":", bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 14)).grid(row=0, column=3)
        tk.Entry(input_box, textvariable=self.sec_var, **entry_style).grid(row=0, column=4, padx=4)

        btn_box = tk.Frame(frame, bg="#1e1e2e")
        btn_box.pack()

        self.tm_start_btn = tk.Button(btn_box, text="Start", width=9, command=self._toggle_timer, bg="#89b4fa", fg="#11111b", font=("Segoe UI", 10, "bold"), bd=0, pady=6, cursor="hand2")
        self.tm_start_btn.grid(row=0, column=0, padx=6)

        tk.Button(btn_box, text="Reset", width=9, command=self._reset_timer, bg="#f38ba8", fg="#11111b", font=("Segoe UI", 10, "bold"), bd=0, pady=6, cursor="hand2").grid(row=0, column=1, padx=6)

    def _toggle_timer(self):
        if not self.tm_running:
            if self.tm_remaining <= 0:
                try:
                    hrs = int(self.hr_var.get() or 0)
                    mins = int(self.min_var.get() or 0)
                    secs = int(self.sec_var.get() or 0)
                    self.tm_remaining = hrs * 3600 + mins * 60 + secs
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")
                    return

            if self.tm_remaining > 0:
                self.tm_running = True
                self.tm_start_btn.config(text="Pause", bg="#f9e2af")
                self._update_timer()
        else:
            self.tm_running = False
            self.tm_start_btn.config(text="Resume", bg="#89b4fa")

    def _reset_timer(self):
        self.tm_running = False
        self.tm_remaining = 0
        self.tm_label.config(text="00:00:00")
        self.tm_start_btn.config(text="Start", bg="#89b4fa")

    def _update_timer(self):
        if self.tm_running:
            if self.tm_remaining > 0:
                mins, secs = divmod(self.tm_remaining, 60)
                hours, mins = divmod(mins, 60)
                self.tm_label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
                self.tm_remaining -= 1
                self.root.after(1000, self._update_timer)
            else:
                self.tm_label.config(text="00:00:00")
                self.tm_running = False
                self.tm_start_btn.config(text="Start", bg="#89b4fa")
                self.root.bell()  # Plays system alert sound
                messagebox.showinfo("Time's Up!", "Countdown timer has finished.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClockApp(root)
    root.mainloop()