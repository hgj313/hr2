import { ProjectManagement } from "@/components/projects/project-management"

export default function ProjectsPage() {
  return (
    <div className="flex-1 space-y-6 p-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">园林施工项目管理</h1>
        <p className="text-muted-foreground">管理园林景观施工项目、团队调配和工程进度跟踪</p>
      </div>
      <ProjectManagement />
    </div>
  )
}
