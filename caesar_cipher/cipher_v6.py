import tkinter as tk
from tkinter import messagebox

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("扩展凯撒密码 - 专业版 v5.0")
        self.root.geometry("1200x675")
        
        # 字符集定义
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789"
        self.symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?/ "
        self.alphabet = list(self.letters + self.digits + self.symbols)

        # 核心变量
        self.shift_var = tk.IntVar(value=3)
        self.mode_var = tk.StringVar(value="encode")

        self._setup_ui()
        
        # 实时预览监听
        self.shift_var.trace_add("write", lambda *args: self.live_update())
        self.text_input.bind("<KeyRelease>", lambda *args: self.live_update())

    def _create_scrolled_text(self, parent, height, font, **kwargs):
        """辅助方法：创建带加粗滚动条的文本框"""
        frame = tk.Frame(parent)
        bar_width = 30 
        scrollbar = tk.Scrollbar(frame, width=bar_width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget = tk.Text(frame, height=height, font=font, 
                              yscrollcommand=scrollbar.set, **kwargs)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        return frame, text_widget
    
    def _setup_ui(self):
        large_font = ("Arial", 16)
        
        # 1. 标题
        tk.Label(self.root, text="扩展凯撒密码 (实时预览 + 滚动支持)", 
                 font=("微软雅黑", 20, "italic"), fg="#2E7D32").pack(pady=5)
        
    # 2. 模式选择 (改造为大方块下沉式按钮)
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=5)

        # 定义大方块样式：取消指示器 (indicatoron=0)
        # selectcolor 定义选中时的颜色，这里使用稍浅的绿色/蓝色以示区别
        btn_style = {
            "variable": self.mode_var,
            "command": self.live_update,
            "font": ("微软雅黑", 12, "bold"),
            "width": 20,           # 宽度与“一键复制”对齐
            "height": 1,           # 增加高度
            "indicatoron": 0,      # 核心修改：使外观变为方块按钮
            "cursor": "hand2",     # 鼠标悬停变手型
            "bd": 4                # 增加边框宽度使下沉效果更明显
        }

        # 加密模式按钮
        tk.Radiobutton(mode_frame, text="加密模式", value="encode", 
                       selectcolor="#E8F5E9",  # 选中时的背景微调
                       **btn_style).pack(side=tk.LEFT, padx=20)
        
        # 解密模式按钮
        tk.Radiobutton(mode_frame, text="解密模式", value="decode", 
                       selectcolor="#E3F2FD",  # 选中时的背景微调
                       **btn_style).pack(side=tk.LEFT, padx=20)

        # 3. 消息输入区
        tk.Label(self.root, text="请输入原文/密文:", font=("微软雅黑", 18, "bold")).pack(pady=5)
        self.input_frame, self.text_input = self._create_scrolled_text(self.root, 6, large_font, width=80)
        self.input_frame.pack(pady=5)

       # 4. 偏移量控制区 (调整为并列布局)
        # 创建一个水平容器
        shift_header_frame = tk.Frame(self.root)
        shift_header_frame.pack(pady=5)

        # 标签靠左排列
        tk.Label(shift_header_frame, text="设置偏移量 (Shift):", 
                 font=("微软雅黑", 18, "bold")).pack(side=tk.LEFT, padx=10)
        
        # 数字输入框紧随其后靠左排列
        self.shift_entry = tk.Entry(shift_header_frame, width=10, font=large_font, 
                                   textvariable=self.shift_var, justify='center')
        self.shift_entry.pack(side=tk.LEFT)

        # 滑动条依然独占一行，排在下方
        self.shift_slider = tk.Scale(self.root, from_=0, to=len(self.alphabet) - 1, 
                                     orient=tk.HORIZONTAL, length=600, variable=self.shift_var)
        self.shift_slider.pack(pady=5)

        # 5. 结果显示区
        tk.Label(self.root, text="实时处理结果:", font=("微软雅黑", 15, "bold"), fg="#1976D2").pack(pady=5)
        self.output_frame, self.result_display = self._create_scrolled_text(
            self.root, 6, large_font, width=80, state='disabled', bg="#f0f0f0", fg="#1565C0")
        self.output_frame.pack(pady=5)

        # 6. 功能按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="一键复制结果", command=self.copy_to_clipboard, 
                  bg="#FF9800", fg="white", font=("微软雅黑", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="清空输入内容", command=self.clear_input, 
                  bg="#F44336", fg="white", font=("微软雅黑", 12, "bold"), width=20).pack(side=tk.LEFT, padx=10)

    def _process_text(self, text, shift, mode):
        if mode == "decode": shift = -shift
        result = ""
        processed_text = text.lower()
        total_len = len(self.alphabet)
        for char in processed_text:
            if char in self.alphabet:
                i = self.alphabet.index(char)
                result += self.alphabet[(i + shift) % total_len]
            else:
                result += char  
        return result

    def live_update(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._display_result("")
            return
        try:
            res = self._process_text(text, self.shift_var.get(), self.mode_var.get())
            self._display_result(res)
        except: pass

    def _display_result(self, result):
        self.result_display.config(state='normal')
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(tk.END, result)
        self.result_display.config(state='disabled')

    def copy_to_clipboard(self):
        result = self.result_display.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已成功复制到剪贴板！")
        else:
            messagebox.showwarning("提示", "结果栏为空，无可复制内容。")

    def clear_input(self):
        self.text_input.delete("1.0", tk.END)
        self.live_update()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()