import tkinter as tk
from tkinter import messagebox

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Extended Caesar Cipher v2.0")
        self.root.geometry("1200x750")
        
        # 定义扩展字符集：字母 + 数字 + 常用符号
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.digits = "0123456789"
        self.symbols = "!@#$%^&*()-_=+[]{}|;:',.<>?/ "
        
        # 构造完整的查找序列
        self.alphabet = list(self.letters + self.digits + self.symbols)

        self._setup_ui()

    # ... [UI代码保持一致，此处省略以节省篇幅] ...

    def _process_text(self, text, shift, mode):
        """
        核心逻辑处理：支持多字符集映射
        数学原理：new_index = (old_index + shift) % total_length
        """
        if mode == "decode":
            shift = -shift
            
        result = ""
        # 转换为小写处理，以匹配 alphabet 序列
        processed_text = text.lower()
        
        total_len = len(self.alphabet)
        
        for char in processed_text:
            if char in self.alphabet:
                # 1. 查找当前字符索引
                i = self.alphabet.index(char)
                # 2. 执行模运算位移
                new_index = (i + shift) % total_len
                # 3. 拼接结果
                result += self.alphabet[new_index]
            else:
                # 字符不在定义的集合中（如换行符或特殊表情），保持原样
                result += char  
        return result

    # ... [其他辅助方法 _get_inputs, handle_encrypt 等保持不变] ...
    
    def _setup_ui(self):
        large_font = ("Arial", 16)
        # 增加一个字符集范围的提示
        tk.Label(self.root, text="Extended Caesar Cipher (Supports a-z, 0-9, and symbols)", 
                 font=("Arial", 20, "italic"), fg="gray").pack(pady=5)
        
        tk.Label(self.root, text="Enter Message:", font=("Arial", 20, "bold")).pack(pady=5)
        self.text_input = tk.Text(self.root, height=8, width=80, font= large_font)
        self.text_input.pack(pady=5)

        tk.Label(self.root, text="Shift Number:", font=("Arial", 20, "bold")).pack(pady=5)
        self.shift_input = tk.Entry(self.root, width=40)
        self.shift_input.insert(0, "3")
        self.shift_input.pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Encode Message", command=self.handle_encrypt, 
                  bg="#4CAF50", fg="white", width=30, height=2).grid(row=0, column=0, padx=40)
        
        tk.Button(btn_frame, text="Decode Message", command=self.handle_decrypt, 
                  bg="#2196F3", fg="white", width=30, height=2).grid(row=0, column=1, padx=40)

        tk.Label(self.root, text="Result:", font=("Arial", 10, "bold")).pack(pady=5)
        self.result_display = tk.Text(self.root, height=8, width=80, state='disabled', bg="#f0f0f0", font=large_font)
        self.result_display.pack(pady=5)

    def _get_inputs(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            return None, None
        try:
            shift = int(self.shift_input.get())
            return text, shift
        except ValueError:
            messagebox.showerror("Error", "Shift Number must be an integer!")
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