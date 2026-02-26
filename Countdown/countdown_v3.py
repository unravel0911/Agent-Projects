import tkinter as tk
from tkinter import messagebox

class FixedCountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fixed Timer v4.1")
        self.root.geometry("400x320")
        
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False
        self.timer_id = None
        
        self.time_display = tk.StringVar(value="00:00")
        self.input_val = tk.StringVar(value="10")
        
        self._setup_ui()

    def _setup_ui(self):
        # UI 布局保持不变
        self.label_time = tk.Label(self.root, textvariable=self.time_display, 
                                 font=("Helvetica", 60, "bold"))
        self.label_time.pack(pady=20)

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5)
        tk.Label(input_frame, text="Step (sec):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_val, width=5).pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Start/Set", command=self.start_timer, width=10).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="+ Add", command=self.add_time, width=10).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="- Sub", command=self.sub_time, width=10).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_timer, width=10).grid(row=1, column=1, pady=10)

    def update_display(self):
        if self.is_running:
            if self.remaining_seconds > 0:
                mins, secs = divmod(self.remaining_seconds, 60)
                self.time_display.set(f"{mins:02d}:{secs:02d}")
                self.remaining_seconds -= 1
                self.timer_id = self.root.after(1000, self.update_display)
            else:
                # 关键修复点：当减到 0 时，立即触发重置逻辑
                self._handle_completion()

    def _handle_completion(self):
        """处理计时结束，清理状态"""
        self.is_running = False
        self.remaining_seconds = 0  # 强制归零，防止非法加时累加
        self.time_display.set("00:00")
        self.root.bell()
        messagebox.showinfo("Time Up", "Timer finished and state reset.")

    def start_timer(self):
        # 修复逻辑：只有在非运行状态下才允许从输入框重新加载
        if not self.is_running:
            try:
                # 如果当前已经是 0，则从输入框重新读取初始时长
                if self.remaining_seconds <= 0:
                    val = int(self.input_val.get())
                    if val <= 0: raise ValueError
                    self.remaining_seconds = val
                    self.total_seconds = val
                
                self.is_running = True
                self.update_display()
            except ValueError:
                messagebox.showerror("Error", "Please enter a positive integer")

    def add_time(self):
        # 增加逻辑判断：只有在运行中或已设置时长的情况下才允许加时
        try:
            inc = int(self.input_val.get())
            self.remaining_seconds += inc
            # 如果是在 0 秒状态下点加时，同步更新 total 以便颜色计算准确
            if self.total_seconds == 0 or self.remaining_seconds > self.total_seconds:
                self.total_seconds = self.remaining_seconds
            
            # 如果计时已经停止但用户点了加时，自动更新一次显示
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
        except ValueError: pass

    def sub_time(self):
        try:
            dec = int(self.input_val.get())
            self.remaining_seconds = max(0, self.remaining_seconds - dec)
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
        except ValueError: pass

    def reset_timer(self):
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.time_display.set("00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = FixedCountdownApp(root)
    root.mainloop()