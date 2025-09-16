import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
  HomeIcon,
  ClockIcon,
  UsersIcon,
  Bars3Icon,
  XMarkIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';
import '../styles/chinese-minimal.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: '仪表板', href: '/', icon: HomeIcon },
    { name: '项目时间轴', href: '/timeline', icon: ClockIcon },
    { name: '用户管理', href: '/users', icon: UsersIcon },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="h-screen flex overflow-hidden ink-wash-bg" style={{background: 'var(--rice-cream)'}}>
      {/* 移动端侧边栏 */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0" style={{background: 'rgba(26, 26, 26, 0.5)'}} onClick={() => setSidebarOpen(false)} />
        <div className="relative flex-1 flex flex-col max-w-xs w-full sidebar-minimal">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full"
              style={{background: 'var(--bamboo-medium)', color: 'var(--rice-white)'}}
              onClick={() => setSidebarOpen(false)}
            >
              <XMarkIcon style={{width: '1.5rem', height: '1.5rem'}} />
            </button>
          </div>
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4 seal-accent">
              <h1 style={{fontSize: '1.25rem', fontWeight: '600', color: 'var(--ink-dark)'}}>HR调度系统</h1>
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className="nav-item group flex items-center px-3 py-3 text-base font-medium rounded-lg transition-all duration-200"
                    style={{
                      background: isActive ? 'var(--bamboo-light)' : 'transparent',
                      color: isActive ? 'var(--ink-dark)' : 'var(--ink-medium)',
                      borderLeft: isActive ? '3px solid var(--bamboo-medium)' : '3px solid transparent'
                    }}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon 
                      style={{
                        marginRight: '1rem', 
                        width: '1.5rem', 
                        height: '1.5rem',
                        color: isActive ? 'var(--bamboo-medium)' : 'var(--ink-light)'
                      }} 
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
          <div className="flex-shrink-0 flex p-4" style={{borderTop: '1px solid var(--bamboo-light)'}}>
            <div className="flex items-center w-full">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full seal-accent flex items-center justify-center" style={{background: 'var(--bamboo-medium)'}}>
                  <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--rice-white)'}}>
                    {user?.username?.charAt(0).toUpperCase()}
                  </span>
                </div>
              </div>
              <div className="ml-3 flex-1">
                <p style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>{user?.username}</p>
                <button
                  onClick={handleLogout}
                  className="flex items-center transition-colors duration-200"
                  style={{fontSize: '0.75rem', color: 'var(--ink-light)', marginTop: '0.25rem'}}
                >
                  <ArrowRightOnRectangleIcon style={{width: '0.75rem', height: '0.75rem', marginRight: '0.25rem'}} />
                  退出登录
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 桌面端侧边栏 */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col h-0 flex-1 sidebar-minimal" style={{borderRight: '1px solid var(--bamboo-light)'}}>
            <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
              <div className="flex items-center flex-shrink-0 px-4 seal-accent">
                <h1 style={{fontSize: '1.25rem', fontWeight: '600', color: 'var(--ink-dark)'}}>HR调度系统</h1>
              </div>
              <nav className="mt-5 flex-1 px-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className="nav-item group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-200"
                      style={{
                        background: isActive ? 'var(--bamboo-light)' : 'transparent',
                        color: isActive ? 'var(--ink-dark)' : 'var(--ink-medium)',
                        borderLeft: isActive ? '3px solid var(--bamboo-medium)' : '3px solid transparent'
                      }}
                    >
                      <item.icon 
                        style={{
                          marginRight: '0.75rem', 
                          width: '1.25rem', 
                          height: '1.25rem',
                          color: isActive ? 'var(--bamboo-medium)' : 'var(--ink-light)'
                        }} 
                      />
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
            <div className="flex-shrink-0 flex p-4" style={{borderTop: '1px solid var(--bamboo-light)'}}>
              <div className="flex items-center w-full">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full seal-accent flex items-center justify-center" style={{background: 'var(--bamboo-medium)'}}>
                    <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--rice-white)'}}>
                      {user?.username?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="ml-3 flex-1">
                  <p style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>{user?.username}</p>
                  <button
                    onClick={handleLogout}
                    className="flex items-center transition-colors duration-200"
                    style={{fontSize: '0.75rem', color: 'var(--ink-light)', marginTop: '0.25rem'}}
                  >
                    <ArrowRightOnRectangleIcon style={{width: '0.75rem', height: '0.75rem', marginRight: '0.25rem'}} />
                    退出登录
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 主内容区域 */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        {/* 顶部导航栏 */}
        <div className="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
          <button
            type="button"
            className="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md transition-colors duration-200"
            style={{color: 'var(--ink-medium)'}}
            onClick={() => setSidebarOpen(true)}
          >
            <Bars3Icon style={{width: '1.5rem', height: '1.5rem'}} />
          </button>
        </div>
        
        {/* 页面内容 */}
        <main className="flex-1 relative z-0 overflow-y-auto" style={{background: 'var(--rice-cream)'}}>
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8 animate-fade-in-up">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;