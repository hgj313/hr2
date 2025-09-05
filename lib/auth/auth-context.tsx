/**
 * 认证上下文
 * 管理用户登录状态和认证信息
 */

'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../api/services';
import { TokenManager } from '../api/client';
import type { User, LoginRequest } from '../api/types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentials: LoginRequest) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // 检查用户是否已认证
  const isAuthenticated = !!user && !!TokenManager.getAccessToken();

  /**
   * 初始化认证状态
   */
  const initializeAuth = async () => {
    try {
      const token = TokenManager.getAccessToken();
      if (token) {
        // 验证token有效性并获取用户信息
        const response = await api.auth.getProfile();
        setUser(response.data);
      }
    } catch (error) {
      console.error('Failed to initialize auth:', error);
      // Token无效，清除本地存储
      TokenManager.clearTokens();
    } finally {
      setLoading(false);
    }
  };

  /**
   * 用户登录
   */
  const login = async (credentials: LoginRequest): Promise<boolean> => {
    try {
      setLoading(true);
      const response = await api.auth.login(credentials);
      const { access_token, refresh_token, user: userData } = response.data;

      // 存储tokens
      TokenManager.setAccessToken(access_token);
      TokenManager.setRefreshToken(refresh_token);

      // 设置用户信息
      setUser(userData);

      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  /**
   * 用户登出
   */
  const logout = async () => {
    try {
      // 调用后端登出接口
      await api.auth.logout();
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // 无论API调用是否成功，都清除本地状态
      TokenManager.clearTokens();
      setUser(null);
      router.push('/login');
    }
  };

  /**
   * 刷新Token
   */
  const refreshToken = async (): Promise<boolean> => {
    try {
      const refreshToken = TokenManager.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await api.auth.refreshToken({ refresh_token: refreshToken });
      const { access_token, refresh_token: newRefreshToken } = response.data;

      // 更新tokens
      TokenManager.setAccessToken(access_token);
      if (newRefreshToken) {
        TokenManager.setRefreshToken(newRefreshToken);
      }

      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      // 刷新失败，清除tokens并跳转到登录页
      TokenManager.clearTokens();
      setUser(null);
      router.push('/login');
      return false;
    }
  };

  // 组件挂载时初始化认证状态
  useEffect(() => {
    initializeAuth();
  }, []);

  // 监听storage变化，处理多标签页同步
  useEffect(() => {
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'access_token') {
        if (!e.newValue) {
          // Token被清除，用户在其他标签页登出
          setUser(null);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const value: AuthContextType = {
    user,
    loading,
    login,
    logout,
    refreshToken,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * 使用认证上下文的Hook
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

/**
 * 检查用户权限的Hook
 */
export function usePermissions() {
  const { user } = useAuth();

  const hasRole = (role: string): boolean => {
    return user?.roles?.includes(role) ?? false;
  };

  const hasPermission = (permission: string): boolean => {
    return user?.permissions?.includes(permission) ?? false;
  };

  const hasAnyRole = (roles: string[]): boolean => {
    return roles.some(role => hasRole(role));
  };

  const hasAnyPermission = (permissions: string[]): boolean => {
    return permissions.some(permission => hasPermission(permission));
  };

  const isAdmin = (): boolean => {
    return hasRole('admin') || hasRole('super_admin');
  };

  const isManager = (): boolean => {
    return hasRole('manager') || isAdmin();
  };

  return {
    hasRole,
    hasPermission,
    hasAnyRole,
    hasAnyPermission,
    isAdmin,
    isManager,
    roles: user?.roles ?? [],
    permissions: user?.permissions ?? [],
  };
}