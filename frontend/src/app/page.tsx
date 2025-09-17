"use client"

import { useState, useEffect } from "react"
import { LoginForm } from "@/components/auth/login-form"
import { Sidebar } from "@/components/layout/sidebar"
import { PersonnelList } from "@/components/personnel/personnel-list"
import { PersonnelDetail } from "@/components/personnel/personnel-detail"
import { OrganizationChart } from "@/components/personnel/organization-chart"
import { ProjectList } from "@/components/projects/project-list"
import { ProjectDetail } from "@/components/projects/project-detail"
import { DragDropScheduling } from "@/components/scheduling/drag-drop-scheduling"
import { AnalyticsDashboard } from "@/components/analytics/analytics-dashboard"
import { SystemSettings } from "@/components/settings/system-settings"
import { SystemStatus } from "@/components/layout/system-status"
import type { User, Project } from "@/lib/mock-data"
import { getUserById } from "@/lib/mock-data"

export default function HomePage() {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState("dashboard")
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [viewMode, setViewMode] = useState<"list" | "detail" | "org">("list")

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem("currentUser")
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setIsLoading(false)
  }, [])

  const handleLogin = (user: User) => {
    setUser(user)
    localStorage.setItem("currentUser", JSON.stringify(user))
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem("currentUser")
  }

  const handlePageChange = (page: string) => {
    setCurrentPage(page)
    setSelectedUser(null)
    setSelectedProject(null)
    setViewMode("list")
  }

  const handleUserSelect = (user: User) => {
    setSelectedUser(user)
    setViewMode("detail")
  }

  const handleUserSelectById = (userId: string) => {
    const user = getUserById(userId)
    if (user) {
      setSelectedUser(user)
      setViewMode("detail")
    }
  }

  const handleUserEdit = (user: User) => {
    // TODO: Implement user edit functionality
    console.log("Edit user:", user)
  }

  const handleProjectSelect = (project: Project) => {
    setSelectedProject(project)
    setViewMode("detail")
  }

  const handleProjectEdit = (project: Project) => {
    // TODO: Implement project edit functionality
    console.log("Edit project:", project)
  }

  const handleBackToList = () => {
    setSelectedUser(null)
    setSelectedProject(null)
    setViewMode("list")
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-muted-foreground">加载中...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return <LoginForm onLogin={handleLogin} />
  }

  const renderMainContent = () => {
    if (currentPage === "dashboard") {
      return <AnalyticsDashboard />
    }

    if (currentPage === "personnel") {
      if (viewMode === "detail" && selectedUser) {
        return <PersonnelDetail user={selectedUser} onBack={handleBackToList} onEdit={handleUserEdit} />
      }
      if (viewMode === "org") {
        return <OrganizationChart onUserSelect={handleUserSelectById} />
      }
      return <PersonnelList onUserSelect={handleUserSelect} onUserEdit={handleUserEdit} />
    }

    if (currentPage === "projects") {
      if (viewMode === "detail" && selectedProject) {
        return <ProjectDetail project={selectedProject} onBack={handleBackToList} onEdit={handleProjectEdit} />
      }
      return <ProjectList onProjectSelect={handleProjectSelect} onProjectEdit={handleProjectEdit} />
    }

    if (currentPage === "scheduling") {
      return <DragDropScheduling />
    }

    if (currentPage === "analytics") {
      return <AnalyticsDashboard />
    }

    if (currentPage === "settings") {
      return <SystemSettings />
    }

    // Placeholder for other pages
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">功能开发中</h2>
          <p className="text-muted-foreground">该模块正在开发中，敬请期待</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar user={user} currentPage={currentPage} onPageChange={handlePageChange} onLogout={handleLogout} />
      <main className="flex-1 overflow-auto">
        <div className="container mx-auto p-6 max-w-7xl">
          <SystemStatus />

          {currentPage === "personnel" && viewMode === "list" && (
            <div className="mb-6">
              <div className="flex gap-2">
                <button
                  onClick={() => setViewMode("list")}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    viewMode === "list"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground hover:bg-muted/80"
                  }`}
                >
                  人员列表
                </button>
                <button
                  onClick={() => setViewMode("org")}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    viewMode === "org"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground hover:bg-muted/80"
                  }`}
                >
                  组织架构
                </button>
              </div>
            </div>
          )}
          {renderMainContent()}
        </div>
      </main>
    </div>
  )
}
