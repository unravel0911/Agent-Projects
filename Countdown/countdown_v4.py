import tkinter as tk
from tkinter import messagebox
import sys

class AutoExitTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Exit Timer v5")
        self.root.geometry("800x450")
        
        # 逻辑变量
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False
        self.timer_id = None
        
        # UI 变量
        self.time_display = tk.StringVar(value="00:00")
        self.input_val = tk.StringVar(value="10")
        
        self._setup_ui()

    def _setup_ui(self):
        """UI 布局逻辑"""
        # 显示区
        self.label_time = tk.Label(self.root, textvariable=self.time_display, 
                                 font=("Helvetica", 60, "bold"))
        self.label_time.pack(pady=20)

        # 输入与控制区
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Step (sec):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_val, width=8).pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="START", command=self.start_timer, width=12, bg="#c8e6c9").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="+ ADD", command=self.add_time, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="- SUB", command=self.sub_time, width=12).grid(row=0, column=2, padx=5)
        
        # 退出提示说明
        tk.Label(self.root, text="Notice: App will exit automatically when time is up.", 
                 fg="gray", font=("Arial", 9)).pack(side=tk.BOTTOM, pady=10)

    def _get_color(self):
        """颜色判定逻辑"""
        if self.total_seconds <= 0: return "black"
        ratio = self.remaining_seconds / self.total_seconds
        if ratio > 0.6: return "#4CAF50"
        if ratio > 0.3: return "#FF9800"
        if ratio > 0.1: return "#FFEB3B"
        return "#F44336"

    def update_tick(self):
        """核心计时引擎"""
        if self.is_running:
            if self.remaining_seconds > 0:
                mins, secs = divmod(self.remaining_seconds, 60)
                self.time_display.set(f"{mins:02d}:{secs:02d}")
                self.label_time.config(fg=self._get_color())
                
                self.remaining_seconds -= 1
                self.timer_id = self.root.after(1000, self.update_tick)
            else:
                self._handle_completion()

    def _handle_completion(self):
        """
        处理完成逻辑：
        1. 视觉与听觉反馈
        2. 延迟 2 秒后强制退出程序
        """
        self.time_display.set("00:00")
        self.label_time.config(fg="#F44336")
        self.root.bell()
        
        # 修改窗口标题以提示退出
        self.root.title("TIME UP - Closing in 2s...")
        
        # 延迟执行退出，以便用户看到 00:00 状态
        self.root.after(2000, self.safe_exit)

    def start_timer(self):
        if not self.is_running:
            try:
                val = int(self.input_val.get())
                if val <= 0: raise ValueError
                self.remaining_seconds = val
                self.total_seconds = val
                self.is_running = True
                self.update_tick()
            except ValueError:
                messagebox.showerror("Error", "Please enter a positive integer!")

    def add_time(self):
        try:
            inc = int(self.input_val.get())
            self.remaining_seconds += inc
            self.total_seconds += inc
        except ValueError: pass

    def sub_time(self):
        try:
            dec = int(self.input_val.get())
            self.remaining_seconds = max(0, self.remaining_seconds - dec)
        except ValueError: pass

    def safe_exit(self):
        """安全关闭流程"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.destroy() # 关闭 Tk 窗口
        sys.exit() # 终止 Python 进程

if __name__ == "__main__":
    root = tk.Tk()
    # 捕获窗口右上角关闭按钮，确保安全退出
    app = AutoExitTimer(root)
    root.protocol("WM_DELETE_WINDOW", app.safe_exit)
    root.mainloop()