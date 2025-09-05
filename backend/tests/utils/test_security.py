import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    decode_token,
    create_password_reset_token,
    verify_password_reset_token,
    create_email_verification_token,
    verify_email_verification_token,
    generate_csrf_token,
    verify_csrf_token,
    check_password_strength
)
from app.core.config import settings


@pytest.mark.utils
class TestSecurity:
    """安全工具函数测试"""
    
    def test_password_hashing(self):
        """测试密码哈希和验证"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # 验证哈希后的密码不等于原密码
        assert hashed != password
        
        # 验证密码验证功能
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_create_access_token(self):
        """测试创建访问令牌"""
        user_id = 123
        token = create_access_token(user_id=user_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["user_id"] == user_id
        assert payload["type"] == "access"
        assert "exp" in payload
    
    def test_create_access_token_with_custom_expires(self):
        """测试创建带自定义过期时间的访问令牌"""
        user_id = 123
        expires_delta = timedelta(minutes=30)
        token = create_access_token(user_id=user_id, expires_delta=expires_delta)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # 验证过期时间
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        expected_exp = datetime.utcnow() + expires_delta
        
        # 允许1分钟的误差
        assert abs((exp_datetime - expected_exp).total_seconds()) < 60
    
    def test_create_refresh_token(self):
        """测试创建刷新令牌"""
        user_id = 123
        token = create_refresh_token(user_id=user_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["user_id"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
    
    def test_decode_token_success(self):
        """测试成功解码令牌"""
        user_id = 123
        token = create_access_token(user_id=user_id)
        
        payload = decode_token(token)
        
        assert payload is not None
        assert payload["user_id"] == user_id
        assert payload["type"] == "access"
    
    def test_decode_token_invalid(self):
        """测试解码无效令牌"""
        invalid_token = "invalid.token.here"
        
        payload = decode_token(invalid_token)
        
        assert payload is None
    
    def test_decode_token_expired(self):
        """测试解码过期令牌"""
        user_id = 123
        # 创建一个已过期的令牌
        expires_delta = timedelta(seconds=-1)  # 负数表示已过期
        token = create_access_token(user_id=user_id, expires_delta=expires_delta)
        
        payload = decode_token(token)
        
        assert payload is None
    
    def test_create_password_reset_token(self):
        """测试创建密码重置令牌"""
        email = "test@example.com"
        token = create_password_reset_token(email=email)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["email"] == email
        assert payload["type"] == "password_reset"
        assert "exp" in payload
    
    def test_verify_password_reset_token_success(self):
        """测试成功验证密码重置令牌"""
        email = "test@example.com"
        token = create_password_reset_token(email=email)
        
        verified_email = verify_password_reset_token(token)
        
        assert verified_email == email
    
    def test_verify_password_reset_token_invalid(self):
        """测试验证无效密码重置令牌"""
        invalid_token = "invalid.token.here"
        
        verified_email = verify_password_reset_token(invalid_token)
        
        assert verified_email is None
    
    def test_verify_password_reset_token_wrong_type(self):
        """测试验证错误类型的令牌"""
        user_id = 123
        # 创建访问令牌而不是密码重置令牌
        token = create_access_token(user_id=user_id)
        
        verified_email = verify_password_reset_token(token)
        
        assert verified_email is None
    
    def test_create_email_verification_token(self):
        """测试创建邮箱验证令牌"""
        email = "test@example.com"
        token = create_email_verification_token(email=email)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["email"] == email
        assert payload["type"] == "email_verification"
        assert "exp" in payload
    
    def test_verify_email_verification_token_success(self):
        """测试成功验证邮箱验证令牌"""
        email = "test@example.com"
        token = create_email_verification_token(email=email)
        
        verified_email = verify_email_verification_token(token)
        
        assert verified_email == email
    
    def test_verify_email_verification_token_invalid(self):
        """测试验证无效邮箱验证令牌"""
        invalid_token = "invalid.token.here"
        
        verified_email = verify_email_verification_token(invalid_token)
        
        assert verified_email is None
    
    def test_generate_csrf_token(self):
        """测试生成CSRF令牌"""
        session_id = "test_session_123"
        token = generate_csrf_token(session_id=session_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # 解码令牌验证内容
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["session_id"] == session_id
        assert payload["type"] == "csrf"
        assert "exp" in payload
    
    def test_verify_csrf_token_success(self):
        """测试成功验证CSRF令牌"""
        session_id = "test_session_123"
        token = generate_csrf_token(session_id=session_id)
        
        is_valid = verify_csrf_token(token=token, session_id=session_id)
        
        assert is_valid is True
    
    def test_verify_csrf_token_wrong_session(self):
        """测试验证CSRF令牌会话ID不匹配"""
        session_id = "test_session_123"
        token = generate_csrf_token(session_id=session_id)
        
        is_valid = verify_csrf_token(token=token, session_id="different_session")
        
        assert is_valid is False
    
    def test_verify_csrf_token_invalid(self):
        """测试验证无效CSRF令牌"""
        invalid_token = "invalid.token.here"
        session_id = "test_session_123"
        
        is_valid = verify_csrf_token(token=invalid_token, session_id=session_id)
        
        assert is_valid is False
    
    def test_check_password_strength_strong(self):
        """测试强密码检查"""
        strong_passwords = [
            "StrongPassword123!",
            "MySecure@Pass2023",
            "Complex#Password99"
        ]
        
        for password in strong_passwords:
            result = check_password_strength(password)
            assert result["is_strong"] is True
            assert result["score"] >= 4
            assert len(result["issues"]) == 0
    
    def test_check_password_strength_weak(self):
        """测试弱密码检查"""
        weak_passwords = [
            "123456",
            "password",
            "abc123",
            "qwerty"
        ]
        
        for password in weak_passwords:
            result = check_password_strength(password)
            assert result["is_strong"] is False
            assert result["score"] < 4
            assert len(result["issues"]) > 0
    
    def test_check_password_strength_medium(self):
        """测试中等强度密码检查"""
        medium_passwords = [
            "Password123",  # 缺少特殊字符
            "password123!",  # 缺少大写字母
            "PASSWORD123!",  # 缺少小写字母
            "Password!",  # 缺少数字
        ]
        
        for password in medium_passwords:
            result = check_password_strength(password)
            assert result["score"] >= 2
            assert result["score"] < 4
            assert len(result["issues"]) > 0
    
    def test_check_password_strength_too_short(self):
        """测试过短密码检查"""
        short_password = "Abc1!"
        result = check_password_strength(short_password)
        
        assert result["is_strong"] is False
        assert "密码长度至少需要8个字符" in result["issues"]
    
    def test_check_password_strength_common_patterns(self):
        """测试常见模式密码检查"""
        common_patterns = [
            "12345678",
            "abcdefgh",
            "qwertyui",
            "password123"
        ]
        
        for password in common_patterns:
            result = check_password_strength(password)
            assert result["is_strong"] is False
            # 应该包含关于常见模式的警告
            pattern_issues = [issue for issue in result["issues"] 
                            if "常见" in issue or "简单" in issue or "连续" in issue]
            assert len(pattern_issues) > 0
    
    def test_token_expiration_times(self):
        """测试不同类型令牌的过期时间"""
        user_id = 123
        email = "test@example.com"
        session_id = "test_session"
        
        # 创建不同类型的令牌
        access_token = create_access_token(user_id=user_id)
        refresh_token = create_refresh_token(user_id=user_id)
        reset_token = create_password_reset_token(email=email)
        verification_token = create_email_verification_token(email=email)
        csrf_token = generate_csrf_token(session_id=session_id)
        
        # 解码并检查过期时间
        access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        reset_payload = jwt.decode(reset_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        verification_payload = jwt.decode(verification_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        csrf_payload = jwt.decode(csrf_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # 验证刷新令牌的过期时间比访问令牌长
        assert refresh_payload["exp"] > access_payload["exp"]
        
        # 验证所有令牌都有合理的过期时间
        current_time = datetime.utcnow().timestamp()
        assert access_payload["exp"] > current_time
        assert refresh_payload["exp"] > current_time
        assert reset_payload["exp"] > current_time
        assert verification_payload["exp"] > current_time
        assert csrf_payload["exp"] > current_time
    
    def test_password_hash_uniqueness(self):
        """测试相同密码生成不同哈希值"""
        password = "testpassword123"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # 由于使用了盐值，相同密码应该生成不同的哈希值
        assert hash1 != hash2
        
        # 但都应该能验证原密码
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True