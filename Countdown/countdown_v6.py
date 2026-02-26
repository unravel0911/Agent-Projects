import tkinter as tk
from tkinter import messagebox
import sys

class LockedTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Locked Timer v6.1")
        self.root.geometry("800x450")
        
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False
        self.has_finished = False  # 新增：终结锁标志位
        self.timer_id = None
        
        self.time_display = tk.StringVar(value="00:00")
        self.input_val = tk.StringVar(value="10")
        
        self._setup_ui()

    def _setup_ui(self):
        # UI 布局保持与原程序一致
        self.label_time = tk.Label(self.root, textvariable=self.time_display, font=("Helvetica", 60, "bold"))
        self.label_time.pack(pady=20)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Step (sec):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_val, width=8).pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # 按钮样式保持：加时绿，减时红
        tk.Button(btn_frame, text="START", command=self.start_timer, width=12).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="+ ADD", command=self.add_time, width=12, bg="#4CAF50", fg="white").grid(row=1, column=0, padx=5)
        tk.Button(btn_frame, text="- SUB", command=self.sub_time, width=12, bg="#F44336", fg="white").grid(row=1, column=1, padx=5)

        self.status_label = tk.Label(self.root, text="Ready", fg="gray")
        self.status_label.pack(side=tk.BOTTOM, pady=10)

    def _get_dynamic_color(self):
        if self.total_seconds <= 0: return "black"
        ratio = self.remaining_seconds / self.total_seconds
        if ratio > 0.6: return "#2E7D32"
        if ratio > 0.3: return "#EF6C00"
        if ratio > 0.1: return "#FBC02D"
        return "#C62828"

    def update_tick(self):
        if self.is_running:
            if self.remaining_seconds > 0:
                mins, secs = divmod(self.remaining_seconds, 60)
                self.time_display.set(f"{mins:02d}:{secs:02d}")
                self.label_time.config(fg=self._get_dynamic_color())
                self.remaining_seconds -= 1
                self.timer_id = self.root.after(1000, self.update_tick)
            else:
                self._handle_completion()

    def _handle_completion(self):
        self.is_running = False
        self.has_finished = True  # 激活终结锁
        self.remaining_seconds = 0
        self.time_display.set("00:00")
        self.label_time.config(fg="#C62828")
        self.root.bell()
        self.status_label.config(text="Finished. System locking...", fg="#C62828")
        self.root.after(2000, self.safe_exit)

    def start_timer(self):
        if self.has_finished: return # 结束后禁止重新开始
        if not self.is_running:
            try:
                if self.remaining_seconds <= 0:
                    val = int(self.input_val.get())
                    self.remaining_seconds = val
                    self.total_seconds = val
                self.is_running = True
                self.update_tick()
            except ValueError:
                messagebox.showerror("Error", "Invalid Input")

    def add_time(self):
        if self.has_finished:
            # 关键改进：如果已经结束，强制保持显示为 00:00
            self.remaining_seconds = 0
            self.time_display.set("00:00")
            return
        
        try:
            inc = int(self.input_val.get())
            self.remaining_seconds += inc
            if self.remaining_seconds > self.total_seconds:
                self.total_seconds = self.remaining_seconds
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
            self.label_time.config(fg=self._get_dynamic_color())
        except ValueError: pass

    def sub_time(self):
        if self.has_finished:
            self.remaining_seconds = 0
            self.time_display.set("00:00")
            return
            
        try:
            dec = int(self.input_val.get())
            self.remaining_seconds = max(0, self.remaining_seconds - dec)
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
            self.label_time.config(fg=self._get_dynamic_color())
        except ValueError: pass

    def safe_exit(self):
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LockedTimer(root)
    root.mainloop()