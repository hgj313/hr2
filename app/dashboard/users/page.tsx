import { UserManagement } from "@/components/users/user-management"

export default function UsersPage() {
  return (
    <div className="flex-1 space-y-6 p-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">人员管理</h1>
        <p className="text-muted-foreground">管理企业人员信息、技能标签和组织架构</p>
      </div>
      <UserManagement />
    </div>
  )
}
