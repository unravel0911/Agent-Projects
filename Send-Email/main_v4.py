import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# --- 1. 日志与配置：记录程序运行轨迹 ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmailManager:
    """
    邮件管理类：负责连接管理、模板生成与邮件投递
    """
    def __init__(self, sender_email):
        self.sender_email = sender_email
        self.smtp_server = "smtp.qq.com"
        self.port = 465
        # 严密分析：从 Windows 环境变量获取 16 位授权码
        self.auth_code = os.environ.get("password")

    def _build_html_template(self, recipient_name, task_detail, status_code):
        """
        构建正式的 HTML 邮件模板
        """
        # 定义状态颜色逻辑
        status_color = "#28a745" if status_code == "成功" else "#dc3545"
        
        html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #333; border-bottom: 2px solid #007bff; padding-bottom: 15px;">自动化任务执行报告</h2>
                <p style="font-size: 16px; color: #555;">尊敬的 <strong>{recipient_name}</strong>：</p>
                <p style="font-size: 14px; color: #666;">系统已完成预设脚本的运行，以下为详细执行摘要：</p>
                
                <div style="background-color: #f9f9f9; border-left: 4px solid #007bff; padding: 15px; margin: 25px 0;">
                    <p style="margin: 5px 0;"><strong>任务名称：</strong> {task_detail}</p>
                    <p style="margin: 5px 0;"><strong>执行状态：</strong> <span style="color: {status_color}; font-weight: bold;">{status_code}</span></p>
                    <p style="margin: 5px 0;"><strong>服务器节点：</strong> QQ-SMTP-Cluster-01</p>
                </div>
                
                <p style="font-size: 13px; color: #999; margin-top: 30px;">
                    注意：此为系统自动生成的正式邮件，请勿直接回复。如有疑问，请联系系统管理员。
                </p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="text-align: center; color: #bbb; font-size: 12px;">© 2026 自动化实验室 | 清华大学校园网环境测试</p>
            </div>
        </body>
        </html>
        """
        return html

    def send_formal_notification(self, recipient_email, recipient_name):
        """
        执行邮件发送主逻辑
        """
        if not self.auth_code or self.auth_code == "None":
            logging.error("环境变量 'password' 读取失败。请确认已在 Windows 中设置并重启 VS Code。")
            return

        # 1. 准备报文
        subject = "【系统通知】自动化脚本运行结果汇报"
        html_body = self._build_html_template(recipient_name, "SMTP 安全通信稳定性实验", "成功")
        
        msg = MIMEText(html_body, 'html', 'utf-8')
        # formataddr 能在收件箱显示美观的别名
        msg['From'] = formataddr((Header("自动化监控中心", "utf-8").encode(), self.sender_email))
        msg['To'] = formataddr((Header(recipient_name, "utf-8").encode(), recipient_email))
        msg['Subject'] = Header(subject, 'utf-8').encode()

        # 2. 严密的连接处理
        try:
            logging.info(f"正在尝试连接至 {self.smtp_server}:{self.port}...")
            # 使用 with 语句确保 SSL 连接在结束时自动安全关闭
            with smtplib.SMTP_SSL(self.smtp_server, self.port, timeout=15) as server:
                server.login(self.sender_email, self.auth_code)
                logging.info("身份验证成功，正在投递报文...")
                server.sendmail(self.sender_email, [recipient_email], msg.as_string())
            
            logging.info(f"邮件已成功投递至: {recipient_email}")
            
        except smtplib.SMTPAuthenticationError:
            logging.error("认证失败：请检查 16 位授权码是否正确。")
        except smtplib.SMTPConnectError:
            logging.error("网络错误：无法连接到 SMTP 服务器，请检查防火墙或代理。")
        except Exception as e:
            logging.error(f"发送过程中发生未知异常: {e}")

# --- 3. 示例调用 ---
if __name__ == "__main__":
    # 实例化对象
    email_app = EmailManager(sender_email="1849811541@qq.com")
    
    # 目标参数
    target = "wangyang21@mails.tsinghua.edu.cn"
    target_name = "王同学"
    
    # 执行
    email_app.send_formal_notification(target, target_name)