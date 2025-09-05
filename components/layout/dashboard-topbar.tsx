"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Bell, Search, LogOut, User, Settings, Menu } from "lucide-react"
import { useIsMobile } from "@/hooks/use-mobile"

interface DashboardTopbarProps {
  onMobileMenuToggle?: () => void
}

export function DashboardTopbar({ onMobileMenuToggle }: DashboardTopbarProps) {
  const [user] = useState({ name: "管理员", email: "admin@company.com" })
  const router = useRouter()
  const isMobile = useIsMobile()

  const handleLogout = () => {
    localStorage.removeItem("isAuthenticated")
    localStorage.removeItem("user")
    router.push("/login")
  }

  return (
    <header className="flex items-center justify-between px-4 lg:px-6 py-4 bg-background border-b border-border">
      {/* 移动端菜单按钮 */}
      {isMobile && (
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={onMobileMenuToggle}
          className="mr-2 lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </Button>
      )}
      
      <div className="flex items-center space-x-4 flex-1 max-w-md">
        <div className={cn(
          "relative flex-1",
          isMobile && "max-w-[200px]"
        )}>
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <Input 
            placeholder={isMobile ? "搜索..." : "搜索人员、项目..."} 
            className="pl-10" 
          />
        </div>
      </div>

      <div className="flex items-center space-x-2 lg:space-x-4">
        {/* 通知按钮 */}
        <Button variant="ghost" size="sm" className="relative">
          <Bell className="w-4 h-4" />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-accent rounded-full"></span>
        </Button>

        {/* 用户菜单 */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-8 w-8 rounded-full">
              <Avatar className="h-8 w-8">
                <AvatarImage src="/placeholder.svg?height=32&width=32" alt={user.name} />
                <AvatarFallback>管</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56" align="end" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">{user.name}</p>
                <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <User className="mr-2 h-4 w-4" />
              <span>个人资料</span>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              <span>设置</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" />
              <span>退出登录</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}
