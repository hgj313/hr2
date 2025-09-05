import { RouteGuard } from '@/components/auth/route-guard'
import { NotificationCenter } from '@/components/notifications/notification-center'

export default function NotificationsPage() {
  return (
    <RouteGuard requiredRoles={['admin', 'manager', 'employee']}>
      <div className="container mx-auto py-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight">通知中心</h1>
          <p className="text-muted-foreground">
            管理您的系统通知和消息
          </p>
        </div>
        <NotificationCenter />
      </div>
    </RouteGuard>
  )
}