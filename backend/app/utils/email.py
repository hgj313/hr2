import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# 邮件模板环境
template_env = Environment(
    loader=FileSystemLoader("app/templates/email")
)


class EmailManager:
    """邮件管理器"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_tls = settings.SMTP_TLS
        self.email_from = settings.EMAIL_FROM or settings.SMTP_USERNAME
    
    def _create_smtp_connection(self):
        """创建SMTP连接"""
        if not self.smtp_host:
            raise ValueError("SMTP配置未设置")
        
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_tls:
                server.starttls()
            if self.smtp_username and self.smtp_password:
                server.login(self.smtp_username, self.smtp_password)
            return server
        except Exception as e:
            logger.error(f"创建SMTP连接失败: {e}")
            raise
    
    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """发送邮件"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from
            msg['To'] = ', '.join(to_emails)
            
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            
            # 添加文本内容
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
            
            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 发送邮件
            with self._create_smtp_connection() as server:
                recipients = to_emails + (cc_emails or []) + (bcc_emails or [])
                server.send_message(msg, to_addrs=recipients)
            
            logger.info(f"邮件发送成功: {subject} -> {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False
    
    def send_template_email(
        self,
        to_emails: List[str],
        subject: str,
        template_name: str,
        template_data: dict,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """使用模板发送邮件"""
        try:
            # 渲染HTML模板
            html_template = template_env.get_template(f"{template_name}.html")
            html_content = html_template.render(**template_data)
            
            # 尝试渲染文本模板
            text_content = None
            try:
                text_template = template_env.get_template(f"{template_name}.txt")
                text_content = text_template.render(**template_data)
            except:
                pass  # 文本模板是可选的
            
            return self.send_email(
                to_emails=to_emails,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                cc_emails=cc_emails,
                bcc_emails=bcc_emails
            )
            
        except Exception as e:
            logger.error(f"模板邮件发送失败: {e}")
            return False


# 全局邮件管理器实例
email_manager = EmailManager()


# 便捷函数
async def send_reset_password_email(
    email_to: str,
    username: str,
    token: str
) -> bool:
    """发送密码重置邮件"""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    template_data = {
        "username": username,
        "reset_url": reset_url,
        "app_name": settings.APP_NAME,
        "expire_minutes": settings.RESET_PASSWORD_TOKEN_EXPIRE_MINUTES
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"{settings.APP_NAME} - 密码重置",
        template_name="reset_password",
        template_data=template_data
    )


async def send_verification_email(
    email_to: str,
    username: str,
    token: str
) -> bool:
    """发送邮箱验证邮件"""
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    template_data = {
        "username": username,
        "verification_url": verification_url,
        "app_name": settings.APP_NAME,
        "expire_hours": settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"{settings.APP_NAME} - 邮箱验证",
        template_name="email_verification",
        template_data=template_data
    )


async def send_welcome_email(
    email_to: str,
    username: str
) -> bool:
    """发送欢迎邮件"""
    template_data = {
        "username": username,
        "app_name": settings.APP_NAME,
        "login_url": f"{settings.FRONTEND_URL}/login"
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"欢迎使用 {settings.APP_NAME}",
        template_name="welcome",
        template_data=template_data
    )


async def send_password_changed_notification(
    email_to: str,
    username: str
) -> bool:
    """发送密码修改通知邮件"""
    template_data = {
        "username": username,
        "app_name": settings.APP_NAME,
        "support_email": settings.EMAIL_FROM
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"{settings.APP_NAME} - 密码已修改",
        template_name="password_changed",
        template_data=template_data
    )


async def send_account_locked_notification(
    email_to: str,
    username: str,
    lockout_duration: int
) -> bool:
    """发送账户锁定通知邮件"""
    template_data = {
        "username": username,
        "app_name": settings.APP_NAME,
        "lockout_duration": lockout_duration,
        "support_email": settings.EMAIL_FROM
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"{settings.APP_NAME} - 账户已锁定",
        template_name="account_locked",
        template_data=template_data
    )


async def send_security_alert_email(
    email_to: str,
    username: str,
    alert_type: str,
    details: dict
) -> bool:
    """发送安全警报邮件"""
    template_data = {
        "username": username,
        "app_name": settings.APP_NAME,
        "alert_type": alert_type,
        "details": details,
        "support_email": settings.EMAIL_FROM
    }
    
    return email_manager.send_template_email(
        to_emails=[email_to],
        subject=f"{settings.APP_NAME} - 安全警报",
        template_name="security_alert",
        template_data=template_data
    )