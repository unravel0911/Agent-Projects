import tkinter as tk
from tkinter import messagebox
import sys

class UltimateTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Timer v6")
        self.root.geometry("400x380")
        
        # 内部状态变量
        self.remaining_seconds = 0
        self.total_seconds = 0
        self.is_running = False
        self.timer_id = None
        
        # UI 变量绑定
        self.time_display = tk.StringVar(value="00:00")
        self.input_val = tk.StringVar(value="10")
        
        self._setup_ui()

    def _setup_ui(self):
        """UI 组件布局与色彩定制"""
        # 时间显示标签
        self.label_time = tk.Label(
            self.root, textvariable=self.time_display, 
            font=("Helvetica", 60, "bold"), fg="black"
        )
        self.label_time.pack(pady=20)

        # 步长设置区
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Step (sec):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_val, width=8).pack(side=tk.LEFT)

        # 控制按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # START 按钮
        tk.Button(btn_frame, text="START", command=self.start_timer, 
                  width=12, height=2).grid(row=0, column=0, columnspan=2, pady=5)
        
        # 加时按钮 (绿色)
        tk.Button(btn_frame, text="+ ADD", command=self.add_time, 
                  width=12, bg="#4CAF50", fg="white", activebackground="#45a049").grid(row=1, column=0, padx=5, pady=5)
        
        # 减时按钮 (红色)
        tk.Button(btn_frame, text="- SUB", command=self.sub_time, 
                  width=12, bg="#F44336", fg="white", activebackground="#d32f2f").grid(row=1, column=1, padx=5, pady=5)

        # 状态提示
        self.status_label = tk.Label(self.root, text="Ready", fg="gray")
        self.status_label.pack(side=tk.BOTTOM, pady=10)

    def _get_dynamic_color(self):
        """实现分时段不同颜色显示逻辑"""
        if self.total_seconds <= 0: return "black"
        
        ratio = self.remaining_seconds / self.total_seconds
        if ratio > 0.6: return "#2E7D32"   # 60%以上：绿色
        if ratio > 0.3: return "#EF6C00"   # 30%以上：橙色
        if ratio > 0.1: return "#FBC02D"   # 10%以上：黄色
        return "#C62828"                  # 最后10%：红色

    def update_tick(self):
        """核心计时引擎"""
        if self.is_running:
            if self.remaining_seconds > 0:
                mins, secs = divmod(self.remaining_seconds, 60)
                self.time_display.set(f"{mins:02d}:{secs:02d}")
                
                # 更新动态颜色
                current_color = self._get_dynamic_color()
                self.label_time.config(fg=current_color)
                
                self.remaining_seconds -= 1
                self.timer_id = self.root.after(1000, self.update_tick)
            else:
                self._handle_completion()

    def _handle_completion(self):
        """计时结束逻辑：修复状态并准备退出"""
        self.is_running = False
        self.remaining_seconds = 0
        self.time_display.set("00:00")
        self.label_time.config(fg="#C62828") # 最终红色
        
        self.root.bell()
        self.status_label.config(text="Time Up! Closing...", fg="#C62828")
        
        # 2秒后自动退出
        self.root.after(2000, self.safe_exit)

    def start_timer(self):
        if not self.is_running:
            try:
                # 若当前数值归零，则从输入框重新读取
                if self.remaining_seconds <= 0:
                    val = int(self.input_val.get())
                    if val <= 0: raise ValueError
                    self.remaining_seconds = val
                    self.total_seconds = val
                
                self.is_running = True
                self.status_label.config(text="Running...", fg="green")
                self.update_tick()
            except ValueError:
                messagebox.showerror("Error", "Please enter a positive integer!")

    def add_time(self):
        try:
            inc = int(self.input_val.get())
            self.remaining_seconds += inc
            # 动态调整 total 保证颜色比例计算正确
            if self.remaining_seconds > self.total_seconds:
                self.total_seconds = self.remaining_seconds
            
            # 即时刷新 UI
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
            self.label_time.config(fg=self._get_dynamic_color())
        except ValueError: pass

    def sub_time(self):
        try:
            dec = int(self.input_val.get())
            self.remaining_seconds = max(0, self.remaining_seconds - dec)
            
            # 即时刷新 UI
            mins, secs = divmod(self.remaining_seconds, 60)
            self.time_display.set(f"{mins:02d}:{secs:02d}")
            self.label_time.config(fg=self._get_dynamic_color())
        except ValueError: pass

    def safe_exit(self):
        """彻底清理并退出"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTimer(root)
    # 绑定窗口关闭协议
    root.protocol("WM_DELETE_WINDOW", app.safe_exit)
    root.mainloop()