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
        self.root.title("Python 高级邮件批量发送系统 v3.1")
        self.root.geometry("1400x750") # 调整窗口高度以适应滚动条布局
        self.attachment_path = None

        # --- 界面元素构建 ---
        # 1. 发件人信息
        tk.Label(root, text="发件人邮箱:", font=("Arial", 15)).pack(pady=5)
        self.sender_entry = tk.Entry(root, width=80, font=("Arial", 12))
        self.sender_entry.insert(0, "1849811541@qq.com")
        self.sender_entry.pack()

        # 2. 多收件人信息
        tk.Label(root, text="收件人列表 (用逗号或分号分隔):", font=("Arial", 15, "bold")).pack(pady=5)
        self.receiver_entry = tk.Entry(root, width=80, font=("Arial", 12))
        self.receiver_entry.insert(0, "wangyang21@mails.tsinghua.edu.cn")
        self.receiver_entry.pack()

        # 3. 邮件主题
        tk.Label(root, text="邮件主题:", font=("Arial", 15)).pack(pady=5)
        self.subject_entry = tk.Entry(root, width=80,font=("Arial", 12) )
        self.subject_entry.pack()

        # 4. 邮件正文 (增加滚动条功能) [关键修改区]
        tk.Label(root, text="邮件正文内容:", font=("Arial", 15)).pack(pady=5)
        
        # 创建一个容器框架，用于包裹 Text 和 Scrollbar
        text_frame = tk.Frame(root)
        text_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # 创建滚动条
        bar_width = 30 
        # scrollbar = tk.Scrollbar(frame, width=bar_width)
        self.scrollbar = tk.Scrollbar(text_frame, width=bar_width)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建文本区域，并绑定滚动条
        # wrap=tk.WORD 确保单词完整换行
        self.text_area = tk.Text(text_frame, width=80, height=15, font=("微软雅黑", 16),
                                 yscrollcommand=self.scrollbar.set, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 设置滚动条控制文本区域视图
        self.scrollbar.config(command=self.text_area.yview)

        # 5. 附件状态
        self.file_label = tk.Label(root, text="未选择附件", fg="gray", font=("Arial", 12))
        self.file_label.pack(pady=5)

        # 6. 按钮控制区
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text=" 📎 上传附件 ", command=self.select_file, width=20, font=("Arial", 12)).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text=" 🚀 立即批量发送 ", command=self.send_batch_mail, 
                  bg="#1a73e8", fg="white", width=25, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=15)

    # --- 以下逻辑维持 main_v8.py 原有功能 ---

    def select_file(self):
        """调用系统对话框选择附件"""
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            file_name = os.path.basename(self.attachment_path)
            self.file_label.config(text=f"已选附件: {file_name}", fg="#28a745")

    def _parse_recipients(self, raw_str):
        """解析收件人字符串，返回地址列表"""
        normalized = raw_str.replace(';', ',')
        addr_list = [addr.strip() for addr in normalized.split(',') if addr.strip()]
        return addr_list

    def _get_html_wrapper(self, content, subject):
        """将内容包装成 HTML 模板"""
        formatted_content = content.replace("\n", "<br>")
        return f"""
        <html>
        <body style="font-family: 'Segoe UI', sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #1a73e8; color: white; padding: 20px; text-align: center;">
                    <h2 style="margin: 0;">{subject}</h2>
                </div>
                <div style="padding: 30px; color: #333; line-height: 1.6;">{formatted_content}</div>
            </div>
        </body>
        </html>
        """

    def send_batch_mail(self):
        """发送逻辑"""
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

        msg.attach(MIMEText(self._get_html_wrapper(body_text, subject), 'html', 'utf-8'))

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