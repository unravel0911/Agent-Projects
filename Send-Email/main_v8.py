import smtplib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

# --- 核心类定义 ---

class MultiRecipientMailer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 高级邮件批量发送系统 v3.0")
        self.root.geometry("1200x675")
        self.attachment_path = None

        # --- 界面元素构建 ---
        # 1. 发件人信息
        tk.Label(root, text="发件人邮箱:", font=("Arial", 15)).pack(pady=5)
        self.sender_entry = tk.Entry(root, width=75)
        self.sender_entry.insert(0, "1849811541@qq.com")
        self.sender_entry.pack()

        # 2. 多收件人信息
        tk.Label(root, text="收件人列表 (多个邮箱请用英文逗号 , 或分号 ; 分隔):", font=("Arial", 15, "bold")).pack(pady=5)
        self.receiver_entry = tk.Entry(root, width=75)
        self.receiver_entry.insert(0, "wangyang21@mails.tsinghua.edu.cn; example@test.com")
        self.receiver_entry.pack()

        # 3. 邮件主题
        tk.Label(root, text="邮件主题:", font=("Arial", 15)).pack(pady=5)
        self.subject_entry = tk.Entry(root, width=75)
        self.subject_entry.pack()

        # 4. 邮件正文 (支持 HTML 转化)
        tk.Label(root, text="邮件正文内容:", font=("Arial", 15)).pack(pady=5)
        self.text_area = tk.Text(root, width=80, height=18, font=("微软雅黑", 10))
        self.text_area.pack()

        # 5. 附件状态
        self.file_label = tk.Label(root, text="未选择附件", fg="gray", font=("Arial", 9))
        self.file_label.pack(pady=5)

        # 6. 按钮控制区
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text=" 📎 上传附件 ", command=self.select_file, width=25).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text=" 🚀 立即批量发送 ", command=self.send_batch_mail, 
                  bg="#1a73e8", fg="white", width=25, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=15)

    def select_file(self):
        """调用系统对话框选择附件"""
        self.attachment_path = filedialog.askopenfilename()
        if self.attachment_path:
            file_name = os.path.basename(self.attachment_path)
            self.file_label.config(text=f"已选附件: {file_name}", fg="#28a745")

    def _parse_recipients(self, raw_str):
        """解析收件人字符串，返回地址列表"""
        # 兼容分号并拆分，去除两端空格，过滤空值
        normalized = raw_str.replace(';', ',')
        addr_list = [addr.strip() for addr in normalized.split(',') if addr.strip()]
        return addr_list

    def _get_html_wrapper(self, content, subject):
        """严密分析：将纯文本内容包装成符合商务规范的 HTML 模板"""
        formatted_content = content.replace("\n", "<br>")
        html_template = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #1a73e8; color: white; padding: 20px; text-align: center;">
                    <h2 style="margin: 0;">{subject}</h2>
                </div>
                <div style="padding: 30px; color: #333; line-height: 1.6;">
                    {formatted_content}
                </div>
                <div style="background-color: #f1f3f4; color: #777; padding: 15px; text-align: center; font-size: 12px;">
                    温馨提示：此邮件为系统自动分发，请勿直接回复。
                </div>
            </div>
        </body>
        </html>
        """
        return html_template

    def send_batch_mail(self):
        """群发核心业务逻辑"""
        # A. 获取界面数据
        sender = self.sender_entry.get().strip()
        raw_receivers = self.receiver_entry.get().strip()
        subject = self.subject_entry.get().strip()
        body_text = self.text_area.get("1.0", tk.END).strip()
        password = os.environ.get("password")

        # B. 数据校验
        recipients = self._parse_recipients(raw_receivers)
        if not recipients:
            messagebox.showwarning("校验失败", "请输入收件人地址！")
            return
        if not password:
            messagebox.showerror("认证错误", "未检测到环境变量 'password'，请先设置授权码。")
            return

        # C. 邮件构造 (MIME 封装)
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = formataddr((Header("自动化分发中心", "utf-8").encode(), sender))
        msg['To'] = ", ".join(recipients)

        # 注入 HTML 正文
        html_body = self._get_html_wrapper(body_text, subject)
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))

        # 注入物理附件
        if self.attachment_path:
            try:
                with open(self.attachment_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    # 解决附件名中文乱码
                    fname = os.path.basename(self.attachment_path)
                    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', fname))
                    msg.attach(part)
            except Exception as e:
                messagebox.showerror("文件读取失败", str(e))
                return

        # D. SMTP 会话与投递
        try:
            # 建立加密连接
            with smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=20) as server:
                server.login(sender, password)
                # 群发核心：recipients 为列表
                server.sendmail(sender, recipients, msg.as_string())
            
            messagebox.showinfo("任务完成", f"邮件已成功批量投递至 {len(recipients)} 个地址！")
        except Exception as e:
            messagebox.showerror("投递中断", f"发送失败原因: {e}")

# --- 4. 程序入口 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiRecipientMailer(root)
    root.mainloop()