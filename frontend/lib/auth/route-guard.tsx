/**
 * 路由守卫组件
 * 保护需要认证的页面和检查用户权限
 */

'use client';

import React, { ReactNode, useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth, usePermissions } from './auth-context';
import { Loader2 } from 'lucide-react';

interface RouteGuardProps {
  children: ReactNode;
  requireAuth?: boolean;
  requiredRoles?: string[];
  requiredPermissions?: string[];
  fallbackPath?: string;
  loadingComponent?: ReactNode;
}

/**
 * 路由守卫组件
 */
export function RouteGuard({
  children,
  requireAuth = true,
  requiredRoles = [],
  requiredPermissions = [],
  fallbackPath = '/login',
  loadingComponent,
}: RouteGuardProps) {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { hasAnyRole, hasAnyPermission } = usePermissions();
  const router = useRouter();
  const pathname = usePathname();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    const checkAccess = async () => {
      // 等待认证状态加载完成
      if (authLoading) {
        return;
      }

      // 如果不需要认证，直接允许访问
      if (!requireAuth) {
        setIsChecking(false);
        return;
      }

      // 检查是否已认证
      if (!isAuthenticated) {
        // 保存当前路径，登录后可以重定向回来
        const returnUrl = encodeURIComponent(pathname);
        router.replace(`${fallbackPath}?returnUrl=${returnUrl}`);
        return;
      }

      // 检查角色权限
      if (requiredRoles.length > 0 && !hasAnyRole(requiredRoles)) {
        router.replace('/unauthorized');
        return;
      }

      // 检查操作权限
      if (requiredPermissions.length > 0 && !hasAnyPermission(requiredPermissions)) {
        router.replace('/unauthorized');
        return;
      }

      // 所有检查通过
      setIsChecking(false);
    };

    checkAccess();
  }, [isAuthenticated, authLoading, requiredRoles, requiredPermissions, pathname, router, fallbackPath, hasAnyRole, hasAnyPermission]);

  // 显示加载状态
  if (authLoading || isChecking) {
    return loadingComponent || <DefaultLoadingComponent />;
  }

  // 渲染子组件
  return <>{children}</>;
}

/**
 * 默认加载组件
 */
function DefaultLoadingComponent() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="flex flex-col items-center space-y-4">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">验证用户权限中...</p>
      </div>
    </div>
  );
}

/**
 * 权限检查组件
 * 用于在组件内部进行权限控制
 */
interface PermissionGuardProps {
  children: ReactNode;
  roles?: string[];
  permissions?: string[];
  fallback?: ReactNode;
  requireAll?: boolean; // 是否需要满足所有条件
}

export function PermissionGuard({
  children,
  roles = [],
  permissions = [],
  fallback = null,
  requireAll = false,
}: PermissionGuardProps) {
  const { hasRole, hasPermission, hasAnyRole, hasAnyPermission } = usePermissions();

  // 检查角色权限
  const hasRequiredRoles = () => {
    if (roles.length === 0) return true;
    return requireAll
      ? roles.every(role => hasRole(role))
      : hasAnyRole(roles);
  };

  // 检查操作权限
  const hasRequiredPermissions = () => {
    if (permissions.length === 0) return true;
    return requireAll
      ? permissions.every(permission => hasPermission(permission))
      : hasAnyPermission(permissions);
  };

  // 检查是否有权限
  const hasAccess = hasRequiredRoles() && hasRequiredPermissions();

  return hasAccess ? <>{children}</> : <>{fallback}</>;
}

/**
 * 管理员权限守卫
 */
export function AdminGuard({ children, fallback }: { children: ReactNode; fallback?: ReactNode }) {
  return (
    <PermissionGuard roles={['admin', 'super_admin']} fallback={fallback}>
      {children}
    </PermissionGuard>
  );
}

/**
 * 经理权限守卫
 */
export function ManagerGuard({ children, fallback }: { children: ReactNode; fallback?: ReactNode }) {
  return (
    <PermissionGuard roles={['manager', 'admin', 'super_admin']} fallback={fallback}>
      {children}
    </PermissionGuard>
  );
}

/**
 * 公共页面守卫（不需要认证）
 */
export function PublicGuard({ children }: { children: ReactNode }) {
  return (
    <RouteGuard requireAuth={false}>
      {children}
    </RouteGuard>
  );
}

/**
 * 认证页面守卫（已登录用户重定向）
 */
export function AuthPageGuard({ children, redirectTo = '/dashboard' }: { children: ReactNode; redirectTo?: string }) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.replace(redirectTo);
    }
  }, [isAuthenticated, loading, router, redirectTo]);

  if (loading) {
    return <DefaultLoadingComponent />;
  }

  if (isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}

/**
 * 高阶组件：为页面添加路由守卫
 */
export function withRouteGuard<P extends object>(
  Component: React.ComponentType<P>,
  guardOptions?: Omit<RouteGuardProps, 'children'>
) {
  return function GuardedComponent(props: P) {
    return (
      <RouteGuard {...guardOptions}>
        <Component {...props} />
      </RouteGuard>
    );
  };
}

/**
 * 高阶组件：为组件添加权限守卫
 */
export function withPermissionGuard<P extends object>(
  Component: React.ComponentType<P>,
  guardOptions?: Omit<PermissionGuardProps, 'children'>
) {
  return function GuardedComponent(props: P) {
    return (
      <PermissionGuard {...guardOptions}>
        <Component {...props} />
      </PermissionGuard>
    );
  };
}