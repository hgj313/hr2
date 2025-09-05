"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { FileText, Download, Share, Calendar } from "lucide-react"

interface SummaryReportProps {
  data: any
}

export function SummaryReport({ data }: SummaryReportProps) {
  const reportSections = [
    {
      title: "执行摘要",
      content: [
        `本月共完成 ${data.overview.completedProjects} 个项目，新启动 ${data.overview.activeProjects} 个项目`,
        `团队整体资源利用率达到 ${data.overview.averageUtilization}%，较上月提升 3%`,
        `项目按时交付率为 ${data.overview.onTimeDelivery}%，超出目标 ${data.overview.onTimeDelivery - 85}%`,
      ],
    },
    {
      title: "关键指标",
      content: [
        `人员效率: 平均每人每月完成 ${((data.overview.completedProjects / data.overview.totalEmployees) * 4).toFixed(1)} 个任务`,
        `成本控制: 项目成本控制在预算的 94% 以内`,
        `客户满意度: 4.2/5.0，较上月提升 0.2 分`,
      ],
    },
    {
      title: "部门表现",
      content: [
        "技术部: 完成 12 个项目，绩效评分 92 分，排名第一",
        "设计部: 完成 8 个项目，绩效评分 88 分，创意指数最高",
        "产品部: 完成 6 个项目，绩效评分 85 分，用户反馈优秀",
      ],
    },
    {
      title: "改进建议",
      content: [
        "建议增加前端开发人员配置，当前需求量较大",
        "优化项目管理流程，减少不必要的会议时间",
        "加强跨部门协作，提升整体项目交付效率",
      ],
    },
  ]

  const handleDownloadReport = () => {
    console.log("[v0] 下载汇总报告")
    // 这里会生成并下载PDF报告
    alert("报告下载功能开发中...")
  }

  const handleShareReport = () => {
    console.log("[v0] 分享汇总报告")
    // 这里会生成分享链接
    alert("报告分享功能开发中...")
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold">月度汇总报告</h3>
          <p className="text-sm text-muted-foreground">报告生成时间: {new Date().toLocaleDateString("zh-CN")}</p>
        </div>

        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={handleShareReport}>
            <Share className="w-4 h-4 mr-2" />
            分享
          </Button>
          <Button onClick={handleDownloadReport} className="bg-primary hover:bg-primary/90">
            <Download className="w-4 h-4 mr-2" />
            下载PDF
          </Button>
        </div>
      </div>

      {/* 报告概览 */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="border-border/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="text-2xl font-bold text-primary">{data.overview.totalProjects}</div>
              <p className="text-sm text-muted-foreground">总项目数</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="text-2xl font-bold text-green-600">{data.overview.completedProjects}</div>
              <p className="text-sm text-muted-foreground">已完成</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="text-2xl font-bold text-blue-600">{data.overview.totalEmployees}</div>
              <p className="text-sm text-muted-foreground">参与人员</p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/50">
          <CardContent className="pt-6">
            <div className="text-center space-y-2">
              <div className="text-2xl font-bold text-orange-600">{data.overview.onTimeDelivery}%</div>
              <p className="text-sm text-muted-foreground">按时交付</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 报告内容 */}
      <div className="grid gap-6 md:grid-cols-2">
        {reportSections.map((section) => (
          <Card key={section.title} className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                {section.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {section.content.map((item, index) => (
                  <div key={index} className="flex items-start space-x-2">
                    <div className="w-1.5 h-1.5 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-muted-foreground leading-relaxed">{item}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 报告状态 */}
      <Card className="border-border/50 bg-muted/20">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm text-muted-foreground">报告周期</span>
              </div>
              <Badge variant="outline">2024年1月</Badge>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-sm text-muted-foreground">
                数据准确性: <span className="font-medium text-green-600">99.8%</span>
              </div>
              <Badge className="bg-green-100 text-green-800">已审核</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
