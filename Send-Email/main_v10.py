import smtplib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

class MultiRecipientMailer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 高级邮件批量发送系统 v3.2")
        self.root.geometry("1400x800") 
        self.attachment_path = None

        # --- 界面元素构建 ---
        tk.Label(root, text="发件人邮箱:", font=("Arial", 15)).pack(pady=5)
        self.sender_entry = tk.Entry(root, width=80, font=("Arial", 12))
        self.sender_entry.insert(0, "1849811541@qq.com")
        self.sender_entry.pack()

        tk.Label(root, text="收件人列表 (用逗号或分号分隔):", font=("Arial", 15, "bold")).pack(pady=5)
        self.receiver_entry = tk.Entry(root, width=80, font=("Arial", 12))
        self.receiver_entry.insert(0, "wangyang21@mails.tsinghua.edu.cn")
        self.receiver_entry.pack()

        tk.Label(root, text="邮件主题:", font=("Arial", 15)).pack(pady=5)
        self.subject_entry = tk.Entry(root, width=80, font=("Arial", 12))
        self.subject_entry.pack()

        # 邮件正文 (含滚动条)
        tk.Label(root, text="邮件正文内容:", font=("Arial", 15)).pack(pady=5)
        text_frame = tk.Frame(root)
        text_frame.pack(pady=5, padx=150, fill=tk.BOTH, expand=True)

        bar_width = 30 
        self.scrollbar = tk.Scrollbar(text_frame, width=bar_width)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(text_frame, width=50, height=15, font=("微软雅黑", 16),
                                 yscrollcommand=self.scrollbar.set, wrap=tk.WORD)
        # self.text_area = tk.Text(text_frame, width=80, height=18, font=("微软雅黑", 10), yscrollcommand=self.scrollbar.set, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_area.yview)

        # --- 【关键修改点：自动显示信头与结尾】 ---
        self.initialize_default_content()

        # 附件状态与按钮
        self.file_label = tk.Label(root, text="未选择附件", fg="gray", font=("Arial", 12))
        self.file_label.pack(pady=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text=" 📎 上传附件 ", command=self.select_file, width=20, font=("Arial", 12)).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text=" 🚀 立即批量发送 ", command=self.send_batch_mail, 
                  bg="#1a73e8", fg="white", width=25, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=15)

    def initialize_default_content(self):
        """严密分析：在窗口打开时，向文本框注入固定的信头、信尾"""
        default_text = (
            "尊敬的 [姓名/招聘办]：\n\n"
            "    您好！\n\n"
            "    [此处输入邮件正文内容...]\n\n"
            "    感谢您在百忙之中抽空阅读，祝您工作顺利！\n\n"
            "此致\n"
            "敬礼！\n\n"
            "王同学\n"
            "清华大学"
        )
        self.text_area.insert("1.0", default_text)

    def select_file(self):
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            file_name = os.path.basename(self.attachment_path)
            self.file_label.config(text=f"已选附件: {file_name}", fg="#28a745")

    def _parse_recipients(self, raw_str):
        normalized = raw_str.replace(';', ',')
        addr_list = [addr.strip() for addr in normalized.split(',') if addr.strip()]
        return addr_list

    def send_batch_mail(self):
        """发送逻辑：修改为一般文本格式 (Plain Text)"""
        sender = self.sender_entry.get().strip()
        raw_receivers = self.receiver_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body_text = self.text_area.get("1.0", tk.END).strip()
        password = os.environ.get("password")

        recipients = self._parse_recipients(raw_receivers)
        if not recipients or not password:
            messagebox.showerror("错误", "请检查收件人地址或环境变量 password 是否设置。")
            return

        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr((Header("自动化分发中心", "utf-8").encode(), sender))
        msg['To'] = ", ".join(recipients)

        # --- 【关键修改点：使用 plain 格式发送】 ---
        # 移除原有的 HTML 包装逻辑，直接附加纯文本
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

        if self.attachment_path:
            try:
                with open(self.attachment_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    fname = os.path.basename(self.attachment_path)
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', fname))
                    msg.attach(part)
            except Exception as e:
                messagebox.showerror("文件失败", str(e))
                return

        try:
            with smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=20) as server:
                server.login(sender, password)
                server.sendmail(sender, recipients, msg.as_string())
            messagebox.showinfo("成功", f"邮件已批量投递至 {len(recipients)} 个地址！")
        except Exception as e:
            messagebox.showerror("失败", f"错误详情: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiRecipientMailer(root)
    root.mainloop()