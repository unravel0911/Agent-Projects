import smtplib
import os
import socket
from email.mime.text import MIMEText
from email.header import Header

# --- 配置 ---
username = "1849811541@qq.com"
receiver_add = "wangyang21@mails.tsinghua.edu.cn"
password = os.environ.get("password")

message = MIMEText("Python SMTP Debugging...", "plain", "utf-8")
message['From'] = username
message['To'] = receiver_add
message['Subject'] = Header("网络环境排查测试", "utf-8")

try:
    print("正在尝试建立 SSL 连接 (Port 465)...")
    # 增加超时设置，防止程序无限期卡死
    socket.setdefaulttimeout(30) 
    
    # 建立连接
    smtp_server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    
    # 【核心修改】开启调试模式，可以在终端看到服务器返回的具体报错码
    smtp_server.set_debuglevel(1)
    
    print("正在登录...")
    smtp_server.login(username, password)
    
    print("正在发送...")
    smtp_server.sendmail(username, [receiver_add], message.as_string())
    print("邮件发送成功！")

except socket.timeout:
    print("错误：网络连接超时，请检查您的网络是否可以访问 smtp.qq.com")
except smtplib.SMTPConnectError:
    print("错误：无法连接到 SMTP 服务器，可能端口被防火墙拦截")
except Exception as e:
    print(f"详细错误信息内容: {e}")

finally:
    if 'smtp_server' in locals() and smtp_server:
        try:
            smtp_server.quit()
        except:
            pass