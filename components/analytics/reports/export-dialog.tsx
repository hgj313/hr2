"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Card, CardContent } from "@/components/ui/card"
import { FileText, Download, Calendar, BarChart3 } from "lucide-react"

interface ExportDialogProps {
  isOpen: boolean
  onClose: () => void
  data: any
}

export function ExportDialog({ isOpen, onClose, data }: ExportDialogProps) {
  const [exportConfig, setExportConfig] = useState({
    format: "pdf",
    timeRange: "current",
    sections: {
      overview: true,
      performance: true,
      resources: true,
      charts: true,
      recommendations: false,
    },
    includeCharts: true,
    includeRawData: false,
  })

  const handleExport = () => {
    console.log("[v0] 导出报告配置:", exportConfig)

    // 模拟导出过程
    const exportData = {
      format: exportConfig.format,
      sections: Object.entries(exportConfig.sections)
        .filter(([_, included]) => included)
        .map(([section, _]) => section),
      timestamp: new Date().toISOString(),
    }

    console.log("[v0] 开始导出报告:", exportData)

    // 这里会调用实际的导出API
    alert(`正在导出 ${exportConfig.format.toUpperCase()} 格式报告...`)

    onClose()
  }

  const handleSectionChange = (section: string, checked: boolean) => {
    setExportConfig((prev) => ({
      ...prev,
      sections: {
        ...prev.sections,
        [section]: checked,
      },
    }))
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Download className="w-5 h-5" />
            导出数据报告
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* 导出格式 */}
          <div className="space-y-3">
            <Label className="text-base font-medium">导出格式</Label>
            <RadioGroup
              value={exportConfig.format}
              onValueChange={(value) => setExportConfig((prev) => ({ ...prev, format: value }))}
            >
              <div className="grid grid-cols-3 gap-4">
                <Card className="cursor-pointer hover:bg-muted/50">
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="pdf" id="pdf" />
                      <Label htmlFor="pdf" className="cursor-pointer flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        PDF报告
                      </Label>
                    </div>
                  </CardContent>
                </Card>

                <Card className="cursor-pointer hover:bg-muted/50">
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="excel" id="excel" />
                      <Label htmlFor="excel" className="cursor-pointer flex items-center gap-2">
                        <BarChart3 className="w-4 h-4" />
                        Excel表格
                      </Label>
                    </div>
                  </CardContent>
                </Card>

                <Card className="cursor-pointer hover:bg-muted/50">
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="csv" id="csv" />
                      <Label htmlFor="csv" className="cursor-pointer flex items-center gap-2">
                        <FileText className="w-4 h-4" />
                        CSV数据
                      </Label>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </RadioGroup>
          </div>

          {/* 时间范围 */}
          <div className="space-y-3">
            <Label className="text-base font-medium">时间范围</Label>
            <Select
              value={exportConfig.timeRange}
              onValueChange={(value) => setExportConfig((prev) => ({ ...prev, timeRange: value }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="选择时间范围" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="current">当前月份</SelectItem>
                <SelectItem value="last3months">最近3个月</SelectItem>
                <SelectItem value="last6months">最近6个月</SelectItem>
                <SelectItem value="lastyear">最近一年</SelectItem>
                <SelectItem value="custom">自定义范围</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* 包含内容 */}
          <div className="space-y-3">
            <Label className="text-base font-medium">包含内容</Label>
            <div className="grid grid-cols-2 gap-4">
              {[
                { key: "overview", label: "概览统计", icon: BarChart3 },
                { key: "performance", label: "绩效分析", icon: Calendar },
                { key: "resources", label: "资源分析", icon: BarChart3 },
                { key: "charts", label: "图表数据", icon: BarChart3 },
              ].map((section) => (
                <div key={section.key} className="flex items-center space-x-2">
                  <Checkbox
                    id={section.key}
                    checked={exportConfig.sections[section.key as keyof typeof exportConfig.sections]}
                    onCheckedChange={(checked) => handleSectionChange(section.key, checked as boolean)}
                  />
                  <Label htmlFor={section.key} className="cursor-pointer flex items-center gap-2">
                    <section.icon className="w-4 h-4" />
                    {section.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>

          {/* 高级选项 */}
          <div className="space-y-3">
            <Label className="text-base font-medium">高级选项</Label>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="includeCharts"
                  checked={exportConfig.includeCharts}
                  onCheckedChange={(checked) =>
                    setExportConfig((prev) => ({ ...prev, includeCharts: checked as boolean }))
                  }
                />
                <Label htmlFor="includeCharts" className="cursor-pointer">
                  包含图表和可视化内容
                </Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="includeRawData"
                  checked={exportConfig.includeRawData}
                  onCheckedChange={(checked) =>
                    setExportConfig((prev) => ({ ...prev, includeRawData: checked as boolean }))
                  }
                />
                <Label htmlFor="includeRawData" className="cursor-pointer">
                  包含原始数据表格
                </Label>
              </div>
            </div>
          </div>

          {/* 预览信息 */}
          <Card className="bg-muted/20">
            <CardContent className="p-4">
              <div className="space-y-2">
                <h4 className="font-medium">导出预览</h4>
                <div className="text-sm text-muted-foreground space-y-1">
                  <p>格式: {exportConfig.format.toUpperCase()}</p>
                  <p>包含章节: {Object.values(exportConfig.sections).filter(Boolean).length} 个</p>
                  <p>预计大小: ~2.5MB</p>
                  <p>生成时间: ~30秒</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="flex justify-end space-x-2 pt-4 border-t">
          <Button variant="outline" onClick={onClose}>
            取消
          </Button>
          <Button onClick={handleExport} className="bg-primary hover:bg-primary/90">
            <Download className="w-4 h-4 mr-2" />
            开始导出
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
