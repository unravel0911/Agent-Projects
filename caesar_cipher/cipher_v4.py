import tkinter as tk
from tkinter import messagebox

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Extended Caesar Cipher v3.0 - Slider Edition")
        self.root.geometry("1200x850") # 增加高度以容纳滑动条
        
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789"
        self.symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?/ "
        self.alphabet = list(self.letters + self.digits + self.symbols)

        # 定义整型变量，用于绑定滑动条和输入框
        self.shift_var = tk.IntVar(value=3)

        self._setup_ui()

    def _setup_ui(self):
        large_font = ("Arial", 16)
        
        # 1. 标题
        tk.Label(self.root, text="Extended Caesar Cipher with Slider", 
                 font=("Arial", 20, "italic"), fg="gray").pack(pady=5)
        
        # 2. 消息输入
        tk.Label(self.root, text="Enter Message:", font=("Arial", 20, "bold")).pack(pady=5)
        self.text_input = tk.Text(self.root, height=6, width=80, font=large_font)
        self.text_input.pack(pady=5)

        # 3. 偏移量控制区 (滑动条 + 输入框)
        tk.Label(self.root, text="Shift Number:", font=("Arial", 20, "bold")).pack(pady=5)
        
        # 滑动条组件：范围 0 到 字符集长度-1
        # orient=tk.HORIZONTAL 表示横向滑动
        self.shift_slider = tk.Scale(
            self.root, 
            from_=0, 
            to=len(self.alphabet) - 1, 
            orient=tk.HORIZONTAL, 
            length=600, 
            variable=self.shift_var, # 绑定变量
            font=("Arial", 12),
            tickinterval=10 # 每隔10个数值显示一个刻度
        )
        self.shift_slider.pack(pady=5)

        # 精确输入框：直接绑定同一个变量 self.shift_var
        self.shift_entry = tk.Entry(self.root, width=10, font=large_font, 
                                   textvariable=self.shift_var, justify='center')
        self.shift_entry.pack(pady=5)

        # 4. 按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Encode Message", command=self.handle_encrypt, 
                  bg="#4CAF50", fg="white", width=25, height=2, font=("Arial", 12, "bold")).grid(row=0, column=0, padx=20)
        tk.Button(btn_frame, text="Decode Message", command=self.handle_decrypt, 
                  bg="#2196F3", fg="white", width=25, height=2, font=("Arial", 12, "bold")).grid(row=0, column=1, padx=20)

        # 5. 结果显示
        tk.Label(self.root, text="Result:", font=("Arial", 15, "bold")).pack(pady=5)
        self.result_display = tk.Text(self.root, height=6, width=80, state='disabled', 
                                     bg="#f0f0f0", font=large_font)
        self.result_display.pack(pady=5)

    def _process_text(self, text, shift, mode):
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

    def _get_inputs(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            return None, None
        try:
            # 直接从绑定的变量获取数值
            shift = self.shift_var.get()
            return text, shift
        except (tk.TclError, ValueError):
            messagebox.showerror("Error", "Please enter a valid integer for Shift!")
            return None, None

    def handle_encrypt(self):
        text, shift = self._get_inputs()
        if text is not None:
            res = self._process_text(text, shift, "encode")
            self._display_result(res)

    def handle_decrypt(self):
        text, shift = self._get_inputs()
        if text is not None:
            res = self._process_text(text, shift, "decode")
            self._display_result(res)

    def _display_result(self, result):
        self.result_display.config(state='normal')
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(tk.END, result)
        self.result_display.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()