"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useIsMobile } from "@/hooks/use-mobile"
import {
  LayoutDashboard,
  Users,
  FolderKanban,
  Calendar,
  BarChart3,
  Settings,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
} from "lucide-react"

const navigation = [
  { name: "仪表盘", href: "/dashboard", icon: LayoutDashboard },
  { name: "人员管理", href: "/dashboard/users", icon: Users },
  { name: "项目管理", href: "/dashboard/projects", icon: FolderKanban },
  { name: "智能调度", href: "/dashboard/scheduling", icon: Calendar },
  { name: "数据分析", href: "/dashboard/analytics", icon: BarChart3 },
  { name: "系统设置", href: "/dashboard/settings", icon: Settings },
]

interface DashboardSidebarProps {
  mobileOpen?: boolean
  onMobileToggle?: () => void
}

export function DashboardSidebar({ mobileOpen = false, onMobileToggle }: DashboardSidebarProps) {
  const [collapsed, setCollapsed] = useState(false)
  const pathname = usePathname()
  const isMobile = useIsMobile()

  // 移动端点击遮罩层关闭菜单
  const handleOverlayClick = () => {
    if (isMobile && onMobileToggle) {
      onMobileToggle()
    }
  }

  // 移动端时自动折叠
  useEffect(() => {
    if (isMobile) {
      setCollapsed(true)
    }
  }, [isMobile])

  return (
    <>
      {/* 移动端遮罩层 */}
      {isMobile && mobileOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/50 lg:hidden" 
          onClick={handleOverlayClick}
        />
      )}
      
      <div
        className={cn(
          "flex flex-col bg-sidebar border-r border-sidebar-border transition-all duration-300",
          // 桌面端样式
          !isMobile && (collapsed ? "w-16" : "w-64"),
          // 移动端样式
          isMobile && [
            "fixed inset-y-0 left-0 z-50 w-64 transform lg:relative lg:translate-x-0",
            mobileOpen ? "translate-x-0" : "-translate-x-full"
          ]
        )}
      >
      <div className="flex items-center justify-between p-4 border-b border-sidebar-border">
        {!collapsed && (
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-sidebar-primary rounded-lg flex items-center justify-center">
              <Users className="w-4 h-4 text-sidebar-primary-foreground" />
            </div>
            <span className="font-semibold text-sidebar-foreground">HR调度系统</span>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            if (isMobile && onMobileToggle) {
              onMobileToggle()
            } else {
              setCollapsed(!collapsed)
            }
          }}
          className="text-sidebar-foreground hover:bg-sidebar-accent"
        >
          {isMobile ? (
            <X className="w-4 h-4" />
          ) : collapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </Button>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          return (
            <Link key={item.name} href={item.href}>
              <Button
                variant={isActive ? "default" : "ghost"}
                className={cn(
                  "w-full justify-start",
                  collapsed ? "px-2" : "px-3",
                  isActive
                    ? "bg-sidebar-primary text-sidebar-primary-foreground hover:bg-sidebar-primary/90"
                    : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                )}
              >
                <item.icon className={cn("w-4 h-4", (collapsed && !isMobile) ? "" : "mr-2")} />
                {(!collapsed || isMobile) && <span>{item.name}</span>}
              </Button>
            </Link>
          )
        })}
      </nav>
    </div>
    </>
  )
}
