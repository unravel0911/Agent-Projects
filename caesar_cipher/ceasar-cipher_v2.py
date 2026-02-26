import tkinter as tk
from tkinter import messagebox

class CaesarCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caesar Cipher v1.0")
        self.root.geometry("1200x675")
        
        self.alphabet = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]

        self._setup_ui()

    def _setup_ui(self):
        # 1. 消息输入区
        tk.Label(self.root, text="Enter Message:", font=("Arial", 20, "bold")).pack(pady=5)
        self.text_input = tk.Text(self.root, height=10, width=80)
        self.text_input.pack(pady=5)

        # 2. 偏移量输入区
        tk.Label(self.root, text="Shift Number:", font=("Arial", 20, "bold")).pack(pady=5)
        self.shift_input = tk.Entry(self.root, width=40)
        self.shift_input.insert(0, "3")  # 默认偏移量
        self.shift_input.pack(pady=5)

        # 3. 按钮区
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # Encode 按钮
        tk.Button(btn_frame, text="Encode Message", command=self.handle_encrypt, 
                  bg="#4CAF50", fg="white", width=30).grid(row=0, column=0, padx=40)
        
        # Decode 按钮
        tk.Button(btn_frame, text="Decode Message", command=self.handle_decrypt, 
                  bg="#2196F3", fg="white", width=30).grid(row=0, column=1, padx=40)

        # 4. 结果显示区
        tk.Label(self.root, text="Result:", font=("Arial", 10, "bold")).pack(pady=5)
        self.result_display = tk.Text(self.root, height=10, width=80, state='disabled', bg="#f0f0f0")
        self.result_display.pack(pady=5)

    def _process_text(self, text, shift, mode):
        """核心逻辑处理"""
        # 如果是解码，将位移取反
        if mode == "decode":
            shift = -shift
            
        result = ""
        for char in text.lower():
            if char in self.alphabet:
                # 计算新索引：(当前索引 + 位移) % 26
                i = self.alphabet.index(char)
                new_index = (i + shift) % 26
                result += self.alphabet[new_index]
            else:
                result += char  # 非字母字符保持不变
        return result

    def _get_inputs(self):
        """获取并验证输入"""
        text = self.text_input.get("1.0", tk.END).strip()
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