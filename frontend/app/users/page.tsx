import { RouteGuard } from "@/lib/auth/route-guard"
import { UserManagement } from "@/components/users/user-management"

export default function UsersPage() {
  return (
    <RouteGuard requiredRoles={["admin", "manager"]}>
      <div className="flex-1 space-y-4 lg:space-y-6 spacing-responsive">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-2 lg:space-y-0">
          <div>
            <h1 className="text-xl lg:text-3xl font-bold tracking-tight text-responsive-xl">用户管理</h1>
            <p className="text-muted-foreground text-responsive mobile-hidden lg:block">
              管理系统用户账号、角色权限和基本信息
            </p>
          </div>
        </div>
        <UserManagement />
      </div>
    </RouteGuard>
  )
}