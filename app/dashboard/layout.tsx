"use client"

import type React from "react"
import { useState } from "react"
import { DashboardSidebar } from "@/components/layout/dashboard-sidebar"
import { DashboardTopbar } from "@/components/layout/dashboard-topbar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleMobileMenuToggle = () => {
    setMobileMenuOpen(!mobileMenuOpen)
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="flex">
        <DashboardSidebar 
          mobileOpen={mobileMenuOpen} 
          onMobileToggle={handleMobileMenuToggle}
        />
        <div className="flex-1 flex flex-col min-w-0">
          <DashboardTopbar onMobileMenuToggle={handleMobileMenuToggle} />
          <main className="flex-1 p-4 lg:p-6 overflow-auto">{children}</main>
        </div>
      </div>
    </div>
  )
}
