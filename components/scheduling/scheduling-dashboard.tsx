"use client"

import { useState } from "react"
import { DragDropScheduler } from "./drag-drop-scheduler"
import { TimelineScheduler } from "./timeline-scheduler"
import { SchedulingConfig } from "./scheduling-config"
import { ConflictResolver } from "./conflict-resolver"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Calendar, Users, Zap, AlertTriangle, Settings, BarChart3 } from "lucide-react"

// 模拟调度数据
const mockSchedulingData = {
  availableStaff: [
    {
      id: "1",
      name: "张三",
      department: "技术部",
      position: "前端工程师",
      skills: ["React", "TypeScript", "Next.js"],
      level: "高级",
      workload: 60,
      availability: "可用",
      hourlyRate: 200,
    },
    {
      id: "2",
      name: "李四",
      department: "技术部",
      position: "后端工程师",
      skills: ["Node.js", "Python", "MySQL"],
      level: "中级",
      workload: 45,
      availability: "可用",
      hourlyRate: 180,
    },
    {
      id: "3",
      name: "王五",
      department: "设计部",
      position: "UI设计师",
      skills: ["Figma", "Photoshop", "Sketch"],
      level: "高级",
      workload: 80,
      availability: "忙碌",
      hourlyRate: 160,
    },
    {
      id: "4",
      name: "赵六",
      department: "产品部",
      position: "产品经理",
      skills: ["产品设计", "需求分析", "Axure"],
      level: "高级",
      workload: 70,
      availability: "可用",
      hourlyRate: 220,
    },
  ],
  projects: [
    {
      id: "1",
      name: "企业官网重构",
      requiredSkills: ["React", "TypeScript", "UI设计"],
      priority: "高",
      deadline: "2024-03-15",
      estimatedHours: 320,
      assignedStaff: [],
      status: "待分配",
    },
    {
      id: "2",
      name: "移动应用开发",
      requiredSkills: ["React Native", "API设计"],
      priority: "中",
      deadline: "2024-05-01",
      estimatedHours: 480,
      assignedStaff: [],
      status: "待分配",
    },
  ],
  conflicts: [
    {
      id: "1",
      type: "时间冲突",
      description: "张三在同一时间段被分配到多个项目",
      severity: "高",
      affectedProjects: ["企业官网重构", "移动应用开发"],
      suggestions: ["调整项目时间线", "分配其他人员"],
    },
    {
      id: "2",
      type: "技能不匹配",
      description: "当前分配的人员技能与项目需求匹配度较低",
      severity: "中",
      affectedProjects: ["移动应用开发"],
      suggestions: ["重新分配具有相关技能的人员", "提供技能培训"],
    },
  ],
}

export function SchedulingDashboard() {
  const [activeTab, setActiveTab] = useState("drag-drop")
  const [schedulingData, setSchedulingData] = useState(mockSchedulingData)
  const [isConfigOpen, setIsConfigOpen] = useState(false)

  // 统计数据
  const stats = {
    totalStaff: schedulingData.availableStaff.length,
    availableStaff: schedulingData.availableStaff.filter((s) => s.availability === "可用").length,
    activeProjects: schedulingData.projects.length,
    conflicts: schedulingData.conflicts.length,
  }

  const handleRunAIScheduling = () => {
    // 模拟AI调度算法
    console.log("[v0] 运行AI智能调度算法...")

    // 这里会调用后端AI调度API
    // 暂时模拟一个简单的匹配逻辑
    const updatedProjects = schedulingData.projects.map((project) => {
      const suitableStaff = schedulingData.availableStaff.filter((staff) => {
        return (
          staff.availability === "可用" &&
          staff.workload < 80 &&
          project.requiredSkills.some((skill) => staff.skills.includes(skill))
        )
      })

      return {
        ...project,
        assignedStaff: suitableStaff.slice(0, 2), // 分配前2个合适的人员
        status: suitableStaff.length > 0 ? "已分配" : "待分配",
      }
    })

    setSchedulingData((prev) => ({
      ...prev,
      projects: updatedProjects,
    }))

    console.log("[v0] AI调度完成，已更新项目分配")
  }

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">可用人员</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">
              {stats.availableStaff}/{stats.totalStaff}
            </div>
            <p className="text-xs text-muted-foreground">人员资源池</p>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">待调度项目</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{stats.activeProjects}</div>
            <p className="text-xs text-muted-foreground">需要分配人员</p>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">调度冲突</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">{stats.conflicts}</div>
            <p className="text-xs text-muted-foreground">需要解决</p>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">匹配效率</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">87%</div>
            <p className="text-xs text-muted-foreground">AI推荐准确率</p>
          </CardContent>
        </Card>
      </div>

      {/* 操作按钮 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button onClick={handleRunAIScheduling} className="bg-primary hover:bg-primary/90">
            <Zap className="w-4 h-4 mr-2" />
            运行AI智能调度
          </Button>
          <Button variant="outline" onClick={() => setIsConfigOpen(true)}>
            <Settings className="w-4 h-4 mr-2" />
            调度配置
          </Button>
        </div>

        {schedulingData.conflicts.length > 0 && (
          <Badge variant="destructive" className="flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            {schedulingData.conflicts.length} 个冲突待解决
          </Badge>
        )}
      </div>

      {/* 调度界面 */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 max-w-md">
          <TabsTrigger value="drag-drop">拖拽调度</TabsTrigger>
          <TabsTrigger value="timeline">时间轴</TabsTrigger>
          <TabsTrigger value="conflicts">冲突解决</TabsTrigger>
        </TabsList>

        <TabsContent value="drag-drop" className="mt-6">
          <DragDropScheduler data={schedulingData} onDataChange={setSchedulingData} />
        </TabsContent>

        <TabsContent value="timeline" className="mt-6">
          <TimelineScheduler data={schedulingData} onDataChange={setSchedulingData} />
        </TabsContent>

        <TabsContent value="conflicts" className="mt-6">
          <ConflictResolver conflicts={schedulingData.conflicts} onResolve={setSchedulingData} />
        </TabsContent>
      </Tabs>

      {/* 调度配置对话框 */}
      {isConfigOpen && <SchedulingConfig isOpen={isConfigOpen} onClose={() => setIsConfigOpen(false)} />}
    </div>
  )
}
