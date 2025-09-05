"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search } from "lucide-react"

interface UserFiltersProps {
  onFilterChange: (filters: any) => void
}

export function UserFilters({ onFilterChange }: UserFiltersProps) {
  const [filters, setFilters] = useState({
    search: "",
    department: "all",
    level: "all",
    status: "all",
  })

  const handleFilterChange = (key: string, value: string) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    onFilterChange(newFilters)
  }

  return (
    <div className="flex items-center space-x-4">
      <div className="relative w-64">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
        <Input
          placeholder="搜索姓名、邮箱、部门..."
          value={filters.search}
          onChange={(e) => handleFilterChange("search", e.target.value)}
          className="pl-10"
        />
      </div>

      <Select value={filters.department} onValueChange={(value) => handleFilterChange("department", value)}>
        <SelectTrigger className="w-32">
          <SelectValue placeholder="部门" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部部门</SelectItem>
          <SelectItem value="技术部">技术部</SelectItem>
          <SelectItem value="设计部">设计部</SelectItem>
          <SelectItem value="产品部">产品部</SelectItem>
          <SelectItem value="运营部">运营部</SelectItem>
        </SelectContent>
      </Select>

      <Select value={filters.level} onValueChange={(value) => handleFilterChange("level", value)}>
        <SelectTrigger className="w-32">
          <SelectValue placeholder="级别" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部级别</SelectItem>
          <SelectItem value="初级">初级</SelectItem>
          <SelectItem value="中级">中级</SelectItem>
          <SelectItem value="高级">高级</SelectItem>
          <SelectItem value="专家">专家</SelectItem>
        </SelectContent>
      </Select>

      <Select value={filters.status} onValueChange={(value) => handleFilterChange("status", value)}>
        <SelectTrigger className="w-32">
          <SelectValue placeholder="状态" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">全部状态</SelectItem>
          <SelectItem value="在职">在职</SelectItem>
          <SelectItem value="离职">离职</SelectItem>
          <SelectItem value="休假">休假</SelectItem>
        </SelectContent>
      </Select>
    </div>
  )
}
