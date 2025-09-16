import React, { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import '../styles/chinese-minimal.css';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, isAuthenticated } = useAuth();

  // 如果已经登录，重定向到首页
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const success = await login(username, password);
      if (!success) {
        setError('用户名或密码错误');
      }
    } catch (error) {
      setError('登录失败，请稍后重试');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center ink-wash-bg" style={{background: 'var(--rice-cream)'}}>
      <div className="max-w-md w-full">
        <div className="card-elevated animate-fade-in-up">
          <div className="text-center mb-xl">
            <div className="mx-auto h-20 w-20 rounded-xl flex items-center justify-center seal-accent" style={{background: 'var(--bamboo-medium)'}}>
              <svg className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="var(--rice-white)" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
            </div>
            <h2 className="mt-lg" style={{fontSize: '1.875rem', fontWeight: '600', color: 'var(--ink-dark)', marginBottom: 'var(--space-sm)'}}>
              人力资源调度系统
            </h2>
            <p style={{color: 'var(--ink-medium)', fontSize: '0.875rem'}}>
              请登录您的账户
          </p>
        </div>
        
          <form onSubmit={handleSubmit}>
            {error && (
              <div className="status-error mb-lg" style={{padding: 'var(--space-md)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-lg)'}}>
                {error}
              </div>
            )}
            
            <div className="mb-lg">
              <label htmlFor="username" style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)', marginBottom: 'var(--space-sm)'}}>
                用户名
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="input-minimal"
                placeholder="请输入用户名"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={isLoading}
              />
            </div>
            
            <div className="mb-xl">
              <label htmlFor="password" style={{display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)', marginBottom: 'var(--space-sm)'}}>
                密码
              </label>
              <div style={{position: 'relative'}}>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="input-minimal"
                  style={{paddingRight: '2.5rem'}}
                  placeholder="请输入密码"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLoading}
                />
                <button
                  type="button"
                  style={{position: 'absolute', top: '50%', right: '0.75rem', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center'}}
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--ink-lighter)'}} />
                  ) : (
                    <EyeIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--ink-lighter)'}} />
                  )}
                </button>
              </div>
            </div>
            
            <div>
              <button
                type="submit"
                disabled={isLoading || !username || !password}
                className="btn-primary-minimal w-full"
                style={{padding: 'var(--space-md) var(--space-lg)', fontSize: '1rem', opacity: (isLoading || !username || !password) ? '0.5' : '1', cursor: (isLoading || !username || !password) ? 'not-allowed' : 'pointer'}}
              >
                {isLoading ? (
                  <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                    <svg style={{animation: 'spin 1s linear infinite', marginRight: 'var(--space-sm)', width: '1.25rem', height: '1.25rem'}} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle style={{opacity: '0.25'}} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path style={{opacity: '0.75'}} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    登录中...
                  </div>
                ) : (
                  '登录'
                )}
              </button>
            </div>
          </form>
          
          <div className="text-center mt-lg">
            <p style={{fontSize: '0.75rem', color: 'var(--ink-lighter)'}}>
              测试账户: admin / 123456
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;