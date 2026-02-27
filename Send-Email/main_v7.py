import smtplib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

class ProfessionalMailer:
    def __init__(self, root):
        self.root = root
        self.root.title("正式邮件 HTML 发送系统")
        self.root.geometry("600x700")
        self.attachment_path = None

        # --- GUI 布局 ---
        # 发件与收件信息
        tk.Label(root, text="发件人 (QQ邮箱):", font=("Arial", 10)).pack(pady=2)
        self.sender_entry = tk.Entry(root, width=60)
        self.sender_entry.insert(0, "1849811541@qq.com")
        self.sender_entry.pack(pady=5)

        tk.Label(root, text="收件人 (目标地址):", font=("Arial", 10)).pack(pady=2)
        self.receiver_entry = tk.Entry(root, width=60)
        self.receiver_entry.insert(0, "wangyang21@mails.tsinghua.edu.cn")
        self.receiver_entry.pack(pady=5)

        tk.Label(root, text="邮件主题 (Subject):", font=("Arial", 10, "bold")).pack(pady=2)
        self.subject_entry = tk.Entry(root, width=60)
        self.subject_entry.pack(pady=5)

        # 正文内容
        tk.Label(root, text="邮件核心内容 (将自动嵌入 HTML 模板):", font=("Arial", 10)).pack(pady=2)
        self.text_area = tk.Text(root, width=60, height=12, font=("微软雅黑", 10))
        self.text_area.pack(pady=5)

        # 附件信息
        self.file_label = tk.Label(root, text="未选择任何附件", fg="gray")
        self.file_label.pack(pady=5)

        # 按钮容器
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text=" 📎 选择附件 ", command=self.select_file, width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text=" 🚀 发送正式邮件 ", command=self.send_mail, bg="#1a73e8", fg="white", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

    def _wrap_in_html_template(self, raw_content, subject):
        """
        严密分析：将用户的纯文本输入包装进精美的 HTML 容器中
        """
        # 将输入框的换行符 \n 替换为 HTML 的 <br>
        html_formatted_content = raw_content.replace("\n", "<br>")
        
        html_template = f"""
        <html>
        <body style="margin: 0; padding: 0; background-color: #f6f9fc; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f6f9fc">
                <tr>
                    <td align="center" style="padding: 20px 0;">
                        <table width="600" border="0" cellspacing="0" cellpadding="0" bgcolor="#ffffff" style="border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            <tr>
                                <td bgcolor="#1a73e8" style="padding: 30px; text-align: center;">
                                    <h1 style="color: #ffffff; margin: 0; font-size: 24px;">{subject}</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 40px; color: #3c4043; line-height: 1.6; font-size: 16px;">
                                    <p style="margin-bottom: 20px;">尊敬的阅信人：</p>
                                    <div style="background-color: #f8f9fa; border-left: 4px solid #1a73e8; padding: 20px; margin: 20px 0;">
                                        {html_formatted_content}
                                    </div>
                                    <p style="margin-top: 30px;">此致，<br>敬礼</p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#f1f3f4" style="padding: 20px; text-align: center; color: #70757a; font-size: 12px;">
                                    此邮件通过 Python 自动化系统发出，具备 HTML 渲染支持。<br>
                                    © 2026 自动化办公实验室
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        return html_template

    def select_file(self):
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            self.file_label.config(text=f"已选附件: {os.path.basename(self.attachment_path)}", fg="#28a745")

    def send_mail(self):
        sender = self.sender_entry.get()
        receiver = self.receiver_entry.get()
        subject = self.subject_entry.get()
        raw_content = self.text_area.get("1.0", tk.END).strip()
        password = os.environ.get("password")

        if not password:
            messagebox.showerror("认证错误", "未发现环境变量 'password'。请在系统中配置 QQ 邮箱授权码。")
            return

        # 1. 构造 MIMEMultipart (混合类型，支持正文+附件)
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr((Header("自动化投递中心", "utf-8").encode(), sender))
        msg['To'] = formataddr((Header("收件人", "utf-8").encode(), receiver))

        # 2. 将正文包装成 HTML 并添加
        html_body = self._wrap_in_html_template(raw_content, subject)
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        # 3. 添加附件
        if self.attachment_path:
            try:
                with open(self.attachment_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    # 处理文件名编码，防止附件中文乱码
                    fname = os.path.basename(self.attachment_path)
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', fname))
                    msg.attach(part)
            except Exception as e:
                messagebox.showerror("读取错误", f"无法加载附件: {e}")
                return

        # 4. 发送逻辑
        try:
            with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, [receiver], msg.as_string())
            messagebox.showinfo("成功", "正式 HTML 邮件及附件已成功发送！")
        except Exception as e:
            messagebox.showerror("发送异常", f"连接或认证失败: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalMailer(root)
    root.mainloop()