import smtplib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class MailerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 企业级邮件发送器")
        self.root.geometry("1200x675")
        self.attachment_path = None

        # --- 界面布局 ---
        # 发件人 (从环境变量读取默认值，也可手动修改)
        tk.Label(root, text="发件人邮箱:").pack(pady=5)
        self.sender_entry = tk.Entry(root, width=50)
        self.sender_entry.insert(0, "1849811541@qq.com")
        self.sender_entry.pack()

        # 收件人
        tk.Label(root, text="收件人邮箱:").pack(pady=5)
        self.receiver_entry = tk.Entry(root, width=50)
        self.receiver_entry.insert(0, "wangyang21@mails.tsinghua.edu.cn")
        self.receiver_entry.pack()

        # 主题
        tk.Label(root, text="邮件主题:").pack(pady=5)
        self.subject_entry = tk.Entry(root, width=50)
        self.subject_entry.pack()

        # 正文
        tk.Label(root, text="邮件正文:").pack(pady=5)
        self.text_area = tk.Text(root, width=50, height=15)
        self.text_area.pack()

        # 附件状态显示
        self.file_label = tk.Label(root, text="未选择附件", fg="grey")
        self.file_label.pack(pady=5)

        # 按钮区
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="上传附件", command=self.select_file).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="发送邮件", command=self.send_mail, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

    def select_file(self):
        """打开文件选择对话框"""
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            file_name = os.path.basename(self.attachment_path)
            self.file_label.config(text=f"已选附件: {file_name}", fg="green")

    def send_mail(self):
        """邮件发送核心逻辑"""
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        subject = self.subject_entry.get()
        content = self.text_area.get("1.0", tk.END)
        password = os.environ.get("password")

        if not password:
            messagebox.showerror("错误", "未检测到环境变量 password (授权码)！")
            return

        # 1. 创建多部分消息容器
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = receiver

        # 2. 添加纯文本正文
        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        # 3. 处理附件逻辑
        if self.attachment_path:
            try:
                with open(self.attachment_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    # 设置附件头，此处用 os.path.basename 获取文件名并防止中文乱码
                    filename = os.path.basename(self.attachment_path)
                    part.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(part)
            except Exception as e:
                messagebox.showerror("文件错误", f"读取附件失败: {e}")
                return

        # 4. 连接服务器并发射
        try:
            with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, [receiver], msg.as_string())
            messagebox.showinfo("成功", "邮件已成功发送！")
        except Exception as e:
            messagebox.showerror("发送失败", f"错误详情: {e}")

# --- 程序入口 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MailerGUI(root)
    root.mainloop()