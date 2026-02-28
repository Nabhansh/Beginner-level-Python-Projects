# ============================================================
# PROJECT 7: Digital Clock (Tkinter GUI)
# ============================================================

import tkinter as tk
from datetime import datetime
import time

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.resizable(False, False)
        self.root.configure(bg="#1A1A2E")
        self.alarm_time = None
        self.alarm_active = False
        self.dark_mode = True
        self.build_ui()
        self.update_clock()

    def build_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#1A1A2E", padx=30, pady=20)
        main_frame.pack()

        # Date label
        self.date_label = tk.Label(main_frame, text="",
                                    font=("Courier New", 16),
                                    bg="#1A1A2E", fg="#A8DADC")
        self.date_label.pack(pady=(0, 5))

        # Clock display
        self.clock_label = tk.Label(main_frame, text="",
                                     font=("Courier New", 72, "bold"),
                                     bg="#1A1A2E", fg="#E94560")
        self.clock_label.pack()

        # Seconds bar
        self.seconds_canvas = tk.Canvas(main_frame, width=400, height=12,
                                         bg="#1A1A2E", highlightthickness=0)
        self.seconds_canvas.pack(pady=5)

        # Day of week
        self.day_label = tk.Label(main_frame, text="",
                                   font=("Courier New", 14),
                                   bg="#1A1A2E", fg="#F5A623")
        self.day_label.pack(pady=(0, 15))

        # Alarm section
        alarm_frame = tk.LabelFrame(main_frame, text=" ⏰ Alarm ",
                                     font=("Arial", 11), bg="#1A1A2E",
                                     fg="#A8DADC", bd=2)
        alarm_frame.pack(fill=tk.X, pady=5)

        inner = tk.Frame(alarm_frame, bg="#1A1A2E")
        inner.pack(pady=8, padx=10)

        tk.Label(inner, text="Set Alarm (HH:MM):", bg="#1A1A2E",
                  fg="white", font=("Arial", 11)).pack(side=tk.LEFT)
        self.alarm_entry = tk.Entry(inner, width=8, font=("Courier New", 14),
                                     bg="#16213E", fg="#E94560",
                                     insertbackground="white", justify=tk.CENTER)
        self.alarm_entry.pack(side=tk.LEFT, padx=8)

        self.alarm_btn = tk.Button(inner, text="Set Alarm", bg="#E94560",
                                    fg="white", font=("Arial", 10),
                                    command=self.set_alarm, padx=8)
        self.alarm_btn.pack(side=tk.LEFT, padx=3)

        self.alarm_status = tk.Label(alarm_frame, text="No alarm set",
                                      font=("Arial", 10), bg="#1A1A2E", fg="#A8DADC")
        self.alarm_status.pack(pady=(0, 8))

        # Toggle button
        tk.Button(main_frame, text="Toggle Theme", bg="#16213E", fg="#A8DADC",
                   font=("Arial", 10), command=self.toggle_theme,
                   padx=10, relief=tk.FLAT).pack(pady=5)

    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%B %d, %Y")
        day_str  = now.strftime("%A")
        seconds  = now.second

        self.clock_label.config(text=time_str)
        self.date_label.config(text=date_str)
        self.day_label.config(text=day_str)

        # Seconds progress bar
        self.seconds_canvas.delete("all")
        w = int(400 * seconds / 59)
        self.seconds_canvas.create_rectangle(0, 0, 400, 12, fill="#16213E")
        self.seconds_canvas.create_rectangle(0, 0, w, 12, fill="#E94560")

        # Check alarm
        if self.alarm_active and self.alarm_time:
            current_hm = now.strftime("%H:%M")
            if current_hm == self.alarm_time and now.second == 0:
                self.trigger_alarm()

        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        alarm_str = self.alarm_entry.get().strip()
        try:
            datetime.strptime(alarm_str, "%H:%M")
            self.alarm_time = alarm_str
            self.alarm_active = True
            self.alarm_status.config(text=f"Alarm set for {alarm_str} ✅", fg="#27AE60")
            self.alarm_btn.config(text="Cancel Alarm", command=self.cancel_alarm)
        except ValueError:
            self.alarm_status.config(text="Invalid format! Use HH:MM (e.g. 07:30)", fg="#E74C3C")

    def cancel_alarm(self):
        self.alarm_active = False
        self.alarm_time = None
        self.alarm_status.config(text="Alarm cancelled", fg="#A8DADC")
        self.alarm_btn.config(text="Set Alarm", command=self.set_alarm)

    def trigger_alarm(self):
        self.alarm_active = False
        for _ in range(3):
            self.root.bell()
        self.alarm_status.config(text="⏰ ALARM! Time to wake up!", fg="#F39C12")
        tk.messagebox = __import__('tkinter.messagebox', fromlist=['messagebox'])
        import tkinter.messagebox as mb
        mb.showinfo("Alarm!", f"⏰ Alarm time! It's {self.alarm_time}")
        self.alarm_btn.config(text="Set Alarm", command=self.set_alarm)

    def toggle_theme(self):
        if self.dark_mode:
            bg, fg1, fg2 = "#F0F0F0", "#333333", "#C0392B"
        else:
            bg, fg1, fg2 = "#1A1A2E", "#A8DADC", "#E94560"
        self.dark_mode = not self.dark_mode
        self.root.configure(bg=bg)
        self.clock_label.configure(bg=bg, fg=fg2)
        self.date_label.configure(bg=bg, fg=fg1)
        self.day_label.configure(bg=bg)
        self.seconds_canvas.configure(bg=bg)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()
