import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# --- 1. 日志配置 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CampusRecruitmentEmail:
    """
    应届生投递系统：集成正式求职模板与自动化发送逻辑
    """
    def __init__(self, sender_email):
        self.sender_email = sender_email
        self.smtp_server = "smtp.qq.com"
        self.port = 465
        self.auth_code = os.environ.get("password")

    def _build_job_application_template(self, hr_name, candidate_name, university, position):
        """
        构建应届生求职专用 HTML 模板
        """
        html = f"""
        <html>
        <body style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #2c3e50;">
            <div style="max-width: 650px; margin: 20px auto; border: 1px solid #e0e6ed; padding: 30px; background-color: #ffffff;">
                <h3 style="color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    应聘申请：{position}
                </h3>
                <p>尊敬的 <strong>{hr_name}</strong>：</p>
                <p>您好！</p>
                <p>我是 <strong>{candidate_name}</strong>，目前就读于 <strong>{university}</strong>。在贵司官网上获知正在招聘 <strong>{position}</strong> 岗位，我对该职位非常感兴趣，特向贵司提交申请。</p>
                
                <div style="background-color: #f4f7f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>个人优势概览：</strong></p>
                    <ul style="margin: 10px 0; color: #57606f;">
                        <li>具备扎实的 Python 开发基础，熟悉自动化脚本编写与 SMTP 协议应用。</li>
                        <li>在校期间多次参与项目实践，拥有良好的团队协作能力与抗压能力。</li>
                        <li>学习能力强，能快速适应高强度的工作节奏。</li>
                    </ul>
                </div>

                <p>随信附上我的个人简历，感谢您在百忙之中抽空审阅。期待能有机会参与面试，与您进一步交流。</p>
                
                <p>此致<br>敬礼！</p>
                
                <div style="margin-top: 40px; border-top: 1px solid #eee; padding-top: 15px; font-size: 13px; color: #7f8c8d;">
                    <p style="margin: 2px 0;"><strong>{candidate_name}</strong></p>
                    <p style="margin: 2px 0;">手机：138-xxxx-xxxx</p>
                    <p style="margin: 2px 0;">邮箱：{self.sender_email}</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def send_job_email(self, hr_email, hr_name, candidate_name, university, position):
        """
        执行求职邮件投递
        """
        if not self.auth_code:
            logging.error("未找到授权码，请确认已设置环境变量 'password'。")
            return

        # 1. 自动生成规范的邮件标题
        subject = f"【校招投递】{candidate_name}-{university}-{position}-一周内到岗"
        
        # 2. 生成 HTML 正文
        body = self._build_job_application_template(hr_name, candidate_name, university, position)
        
        msg = MIMEText(body, 'html', 'utf-8')
        msg['From'] = formataddr((Header(candidate_name, "utf-8").encode(), self.sender_email))
        msg['To'] = formataddr((Header(hr_name, "utf-8").encode(), hr_email))
        msg['Subject'] = Header(subject, 'utf-8').encode()

        # 3. 严密的连接逻辑
        try:
            logging.info(f"正在向 {hr_name} ({hr_email}) 发送求职简历...")
            with smtplib.SMTP_SSL(self.smtp_server, self.port, timeout=15) as server:
                server.login(self.sender_email, self.auth_code)
                server.sendmail(self.sender_email, [hr_email], msg.as_string())
            logging.info("求职邮件投递成功！")
        except Exception as e:
            logging.error(f"投递失败，原因: {e}")

# --- 3. 示例调用 ---
if __name__ == "__main__":
    # 配置发件人
    app = CampusRecruitmentEmail(sender_email="1849811541@qq.com")
    
    # 模拟投递：清华大学应届生王同学申请 Python 开发实习生
    app.send_job_email(
        hr_email="wangyang21@mails.tsinghua.edu.cn", # 测试时发给自己或目标邮箱
        hr_name="清华招聘办",
        candidate_name="王小明",
        university="清华大学",
        position="Python 后端开发工程师"
    )