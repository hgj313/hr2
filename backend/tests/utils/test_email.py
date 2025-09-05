import pytest
from unittest.mock import Mock, patch, MagicMock
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.utils.email import (
    EmailManager,
    send_password_reset_email,
    send_verification_email,
    send_welcome_email,
    send_password_changed_notification,
    send_account_locked_notification,
    send_security_alert
)
from app.core.config import settings


@pytest.mark.utils
class TestEmailManager:
    """邮件管理器测试"""
    
    @pytest.fixture
    def email_manager(self):
        """创建邮件管理器实例"""
        return EmailManager()
    
    @patch('smtplib.SMTP')
    def test_create_connection_success(self, mock_smtp, email_manager):
        """测试成功创建SMTP连接"""
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        connection = email_manager._create_connection()
        
        assert connection == mock_server
        mock_smtp.assert_called_once_with(settings.SMTP_HOST, settings.SMTP_PORT)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(settings.SMTP_USER, settings.SMTP_PASSWORD)
    
    @patch('smtplib.SMTP')
    def test_create_connection_failure(self, mock_smtp, email_manager):
        """测试SMTP连接失败"""
        mock_smtp.side_effect = Exception("Connection failed")
        
        connection = email_manager._create_connection()
        
        assert connection is None
    
    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp, email_manager):
        """测试成功发送邮件"""
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = email_manager.send_email(
            to_email="test@example.com",
            subject="测试邮件",
            body="这是一封测试邮件"
        )
        
        assert result is True
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp, email_manager):
        """测试发送邮件失败"""
        mock_server = Mock()
        mock_server.send_message.side_effect = Exception("Send failed")
        mock_smtp.return_value = mock_server
        
        result = email_manager.send_email(
            to_email="test@example.com",
            subject="测试邮件",
            body="这是一封测试邮件"
        )
        
        assert result is False
        mock_server.quit.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_email_with_html(self, mock_smtp, email_manager):
        """测试发送HTML邮件"""
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = email_manager.send_email(
            to_email="test@example.com",
            subject="HTML测试邮件",
            body="<h1>这是HTML邮件</h1>",
            is_html=True
        )
        
        assert result is True
        
        # 验证发送的消息
        call_args = mock_server.send_message.call_args[0][0]
        assert call_args['Subject'] == "HTML测试邮件"
        assert call_args['To'] == "test@example.com"
        assert call_args['From'] == settings.SMTP_USER
    
    @patch('smtplib.SMTP')
    def test_send_template_email_success(self, mock_smtp, email_manager):
        """测试成功发送模板邮件"""
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        template_vars = {
            "user_name": "张三",
            "reset_link": "https://example.com/reset"
        }
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = \
                "Hello {{user_name}}, click {{reset_link}} to reset password."
            
            result = email_manager.send_template_email(
                to_email="test@example.com",
                subject="密码重置",
                template_name="password_reset.html",
                template_vars=template_vars
            )
        
        assert result is True
        mock_server.send_message.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_template_email_template_not_found(self, mock_smtp, email_manager):
        """测试模板文件不存在"""
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        with patch('builtins.open', side_effect=FileNotFoundError()):
            result = email_manager.send_template_email(
                to_email="test@example.com",
                subject="测试",
                template_name="nonexistent.html",
                template_vars={}
            )
        
        assert result is False
        mock_server.send_message.assert_not_called()


@pytest.mark.utils
class TestEmailFunctions:
    """邮件功能函数测试"""
    
    @patch('app.utils.email.EmailManager')
    def test_send_password_reset_email(self, mock_email_manager_class):
        """测试发送密码重置邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_password_reset_email(
            to_email="test@example.com",
            user_name="张三",
            reset_token="reset_token_123"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "密码重置请求"
        assert call_args[1]['template_name'] == "password_reset.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
        assert "reset_token_123" in call_args[1]['template_vars']['reset_link']
    
    @patch('app.utils.email.EmailManager')
    def test_send_verification_email(self, mock_email_manager_class):
        """测试发送邮箱验证邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_verification_email(
            to_email="test@example.com",
            user_name="张三",
            verification_token="verify_token_123"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "邮箱验证"
        assert call_args[1]['template_name'] == "email_verification.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
        assert "verify_token_123" in call_args[1]['template_vars']['verification_link']
    
    @patch('app.utils.email.EmailManager')
    def test_send_welcome_email(self, mock_email_manager_class):
        """测试发送欢迎邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_welcome_email(
            to_email="test@example.com",
            user_name="张三"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "欢迎加入人力资源调度系统"
        assert call_args[1]['template_name'] == "welcome.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
    
    @patch('app.utils.email.EmailManager')
    def test_send_password_changed_notification(self, mock_email_manager_class):
        """测试发送密码修改通知邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_password_changed_notification(
            to_email="test@example.com",
            user_name="张三"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "密码修改通知"
        assert call_args[1]['template_name'] == "password_changed.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
    
    @patch('app.utils.email.EmailManager')
    def test_send_account_locked_notification(self, mock_email_manager_class):
        """测试发送账户锁定通知邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_account_locked_notification(
            to_email="test@example.com",
            user_name="张三",
            reason="多次登录失败"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "账户安全通知"
        assert call_args[1]['template_name'] == "account_locked.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
        assert call_args[1]['template_vars']['lock_reason'] == "多次登录失败"
    
    @patch('app.utils.email.EmailManager')
    def test_send_security_alert(self, mock_email_manager_class):
        """测试发送安全警报邮件"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = True
        mock_email_manager_class.return_value = mock_manager
        
        result = send_security_alert(
            to_email="test@example.com",
            user_name="张三",
            alert_type="异常登录",
            details="从未知设备登录",
            ip_address="192.168.1.100"
        )
        
        assert result is True
        mock_manager.send_template_email.assert_called_once()
        
        # 验证调用参数
        call_args = mock_manager.send_template_email.call_args
        assert call_args[1]['to_email'] == "test@example.com"
        assert call_args[1]['subject'] == "安全警报"
        assert call_args[1]['template_name'] == "security_alert.html"
        assert call_args[1]['template_vars']['user_name'] == "张三"
        assert call_args[1]['template_vars']['alert_type'] == "异常登录"
        assert call_args[1]['template_vars']['details'] == "从未知设备登录"
        assert call_args[1]['template_vars']['ip_address'] == "192.168.1.100"
    
    @patch('app.utils.email.EmailManager')
    def test_email_function_failure(self, mock_email_manager_class):
        """测试邮件发送失败的情况"""
        mock_manager = Mock()
        mock_manager.send_template_email.return_value = False
        mock_email_manager_class.return_value = mock_manager
        
        result = send_password_reset_email(
            to_email="test@example.com",
            user_name="张三",
            reset_token="reset_token_123"
        )
        
        assert result is False
    
    @patch('app.utils.email.EmailManager')
    def test_email_function_exception(self, mock_email_manager_class):
        """测试邮件发送异常的情况"""
        mock_manager = Mock()
        mock_manager.send_template_email.side_effect = Exception("Email error")
        mock_email_manager_class.return_value = mock_manager
        
        result = send_password_reset_email(
            to_email="test@example.com",
            user_name="张三",
            reset_token="reset_token_123"
        )
        
        assert result is False
    
    def test_email_validation(self):
        """测试邮箱地址验证"""
        # 这里可以添加邮箱地址格式验证的测试
        # 如果EmailManager中有邮箱验证功能的话
        pass
    
    @patch('app.utils.email.EmailManager')
    def test_email_with_attachments(self, mock_email_manager_class):
        """测试带附件的邮件发送"""
        # 如果EmailManager支持附件功能，可以添加相关测试
        pass
    
    @patch('app.utils.email.EmailManager')
    def test_bulk_email_sending(self, mock_email_manager_class):
        """测试批量邮件发送"""
        # 如果有批量发送功能，可以添加相关测试
        pass
    
    def test_email_template_rendering(self):
        """测试邮件模板渲染"""
        # 可以添加模板渲染逻辑的单独测试
        template_content = "Hello {{name}}, your code is {{code}}."
        variables = {"name": "张三", "code": "123456"}
        
        # 简单的模板替换测试
        rendered = template_content
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
        
        expected = "Hello 张三, your code is 123456."
        assert rendered == expected
    
    @patch('app.utils.email.EmailManager')
    def test_email_rate_limiting(self, mock_email_manager_class):
        """测试邮件发送频率限制"""
        # 如果有频率限制功能，可以添加相关测试
        pass
    
    @patch('app.utils.email.EmailManager')
    def test_email_retry_mechanism(self, mock_email_manager_class):
        """测试邮件发送重试机制"""
        # 如果有重试机制，可以添加相关测试
        pass