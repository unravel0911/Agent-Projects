import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header

# --- 配置定义 ---
username = "1849811541@qq.com"
receiver_add = "wangyang21@mails.tsinghua.edu.cn"
# 确保你已经运行了: $env:password="你的16位授权码"
password = os.environ.get("password")

# --- 邮件内容构建 (遵循标准 RFC 格式) ---
message = MIMEText("Hello, this is a test email from Python.", "plain", "utf-8")
message['From'] = username
message['To'] = receiver_add
message['Subject'] = Header("Python SMTP 测试", "utf-8")

# --- 严谨的连接处理逻辑 ---
smtp_server = None
try:
    # 使用 SMTP_SSL 和 465 端口，这是目前最推荐、最稳定的 QQ 邮箱连接方式
    print("Connecting to QQ SMTP server...")
    smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    
    # 身份验证
    smtp_server.login(username, password)
    print("Login successful.")

    # 发送邮件
    smtp_server.sendmail(username, [receiver_add], message.as_string())
    print("Successfully the mail is sent.")

except smtplib.SMTPException as e:
    print(f"SMTP Error: {e}")
except Exception as e:
    print(f"General Error: {e}")

finally:
    # 核心修改：安全地退出
    if smtp_server:
        try:
            smtp_server.quit()
        except smtplib.SMTPServerDisconnected:
            # 如果连接已经关闭，静默处理，不再抛出异常
            pass