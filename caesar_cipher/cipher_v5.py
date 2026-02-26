import tkinter as tk
from tkinter import messagebox

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("扩展凯撒密码 - 实时预览版 v4.1")
        self.root.geometry("1200x675")
        
        # 定义扩展字符集：字母 + 数字 + 常用符号
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789"
        self.symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?/ "
        
        # 构造完整的查找序列
        self.alphabet = list(self.letters + self.digits + self.symbols)

        # 核心变量绑定
        self.shift_var = tk.IntVar(value=3)
        self.mode_var = tk.StringVar(value="encode") # 默认加密模式

        self._setup_ui()
        
        # 建立实时监听
        # 1. 监听位移量变量变化
        self.shift_var.trace_add("write", lambda *args: self.live_update())
        # 2. 监听文本输入框键盘释放事件
        self.text_input.bind("<KeyRelease>", lambda *args: self.live_update())

    def _setup_ui(self):
        large_font = ("Arial", 16)
        
        # 1. 标题与说明
        tk.Label(self.root, text="扩展凯撒密码 (支持字母、数字及常用符号)", 
                 font=("微软雅黑", 20, "italic"), fg="#2E7D32").pack(pady=5)
        
        # 2. 模式选择
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=5)
        tk.Radiobutton(mode_frame, text="加密模式", variable=self.mode_var, value="encode", 
                       command=self.live_update, font=("微软雅黑", 12, "bold")).pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(mode_frame, text="解密模式", variable=self.mode_var, value="decode", 
                       command=self.live_update, font=("微软雅黑", 12, "bold")).pack(side=tk.LEFT, padx=20)

        # 3. 消息输入区
        tk.Label(self.root, text="请输入原文/密文:", font=("微软雅黑", 20, "bold")).pack(pady=5)
        self.text_input = tk.Text(self.root, height=6, width=80, font=large_font)
        self.text_input.pack(pady=5)

        # 4. 偏移量控制区 (滑动条 + 数字输入框)
        tk.Label(self.root, text="设置偏移量 (Shift):", font=("微软雅黑", 20, "bold")).pack(pady=5)
        
        self.shift_slider = tk.Scale(
            self.root, from_=0, to=len(self.alphabet) - 1, 
            orient=tk.HORIZONTAL, length=600, variable=self.shift_var, font=("Arial", 12),
            tickinterval=10
        )
        self.shift_slider.pack(pady=5)

        # 保留数字输入按钮/输入框，并与变量绑定
        self.shift_entry = tk.Entry(self.root, width=10, font=large_font, 
                                   textvariable=self.shift_var, justify='center')
        self.shift_entry.pack(pady=5)

        # 5. 结果显示区
        tk.Label(self.root, text="实时处理结果:", font=("微软雅黑", 15, "bold"), fg="#1976D2").pack(pady=10)
        self.result_display = tk.Text(self.root, height=6, width=80, state='disabled', 
                                     bg="#f0f0f0", font=large_font, fg="#1565C0")
        self.result_display.pack(pady=5)

    def _process_text(self, text, shift, mode):
        """核心处理逻辑"""
        if mode == "decode":
            shift = -shift
            
        result = ""
        processed_text = text.lower()
        total_len = len(self.alphabet)
        
        for char in processed_text:
            if char in self.alphabet:
                i = self.alphabet.index(char)
                new_index = (i + shift) % total_len
                result += self.alphabet[new_index]
            else:
                result += char  
        return result

    def live_update(self):
        """执行实时更新"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self._display_result("")
            return
            
        try:
            # 尝试获取当前偏移量
            shift = self.shift_var.get()
            mode = self.mode_var.get()
            res = self._process_text(text, shift, mode)
            self._display_result(res)
        except (tk.TclError, ValueError):
            # 当用户在输入框中删除数字导致临时为空时，不报错，保持现状
            pass

    def _display_result(self, result):
        self.result_display.config(state='normal')
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(tk.END, result)
        self.result_display.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()