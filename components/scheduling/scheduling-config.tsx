"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Settings, Brain, Target, Clock } from "lucide-react"

interface SchedulingConfigProps {
  isOpen: boolean
  onClose: () => void
}

export function SchedulingConfig({ isOpen, onClose }: SchedulingConfigProps) {
  const [config, setConfig] = useState({
    // AI算法配置
    skillMatchWeight: 70,
    workloadBalanceWeight: 20,
    costOptimizationWeight: 10,
    enableAIRecommendation: true,

    // 约束条件
    maxWorkloadPerPerson: 80,
    minSkillMatchThreshold: 50,
    allowOvertime: false,
    prioritizeExperience: true,

    // 时间配置
    workingHoursPerDay: 8,
    workingDaysPerWeek: 5,
    projectBufferTime: 10,

    // 通知设置
    enableConflictAlerts: true,
    enableWorkloadWarnings: true,
    autoSaveInterval: 5,
  })

  const handleSave = () => {
    console.log("[v0] 保存调度配置:", config)
    // 这里会调用API保存配置
    alert("配置已保存")
    onClose()
  }

  const handleReset = () => {
    console.log("[v0] 重置调度配置")
    // 重置为默认配置
    setConfig({
      skillMatchWeight: 70,
      workloadBalanceWeight: 20,
      costOptimizationWeight: 10,
      enableAIRecommendation: true,
      maxWorkloadPerPerson: 80,
      minSkillMatchThreshold: 50,
      allowOvertime: false,
      prioritizeExperience: true,
      workingHoursPerDay: 8,
      workingDaysPerWeek: 5,
      projectBufferTime: 10,
      enableConflictAlerts: true,
      enableWorkloadWarnings: true,
      autoSaveInterval: 5,
    })
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            智能调度配置
          </DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="algorithm" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="algorithm" className="flex items-center gap-2">
              <Brain className="w-4 h-4" />
              AI算法
            </TabsTrigger>
            <TabsTrigger value="constraints" className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              约束条件
            </TabsTrigger>
            <TabsTrigger value="time" className="flex items-center gap-2">
              <Clock className="w-4 h-4" />
              时间设置
            </TabsTrigger>
            <TabsTrigger value="notifications" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              通知设置
            </TabsTrigger>
          </TabsList>

          <TabsContent value="algorithm" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>AI算法权重配置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>技能匹配权重: {config.skillMatchWeight}%</Label>
                    <Slider
                      value={[config.skillMatchWeight]}
                      onValueChange={([value]) => setConfig((prev) => ({ ...prev, skillMatchWeight: value }))}
                      max={100}
                      step={5}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">权重越高，越优先考虑技能匹配度</p>
                  </div>

                  <div className="space-y-2">
                    <Label>工作负载平衡权重: {config.workloadBalanceWeight}%</Label>
                    <Slider
                      value={[config.workloadBalanceWeight]}
                      onValueChange={([value]) => setConfig((prev) => ({ ...prev, workloadBalanceWeight: value }))}
                      max={100}
                      step={5}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">权重越高，越注重团队工作负载均衡</p>
                  </div>

                  <div className="space-y-2">
                    <Label>成本优化权重: {config.costOptimizationWeight}%</Label>
                    <Slider
                      value={[config.costOptimizationWeight]}
                      onValueChange={([value]) => setConfig((prev) => ({ ...prev, costOptimizationWeight: value }))}
                      max={100}
                      step={5}
                      className="w-full"
                    />
                    <p className="text-xs text-muted-foreground">权重越高，越优先考虑成本控制</p>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <Label>启用AI智能推荐</Label>
                    <p className="text-xs text-muted-foreground">使用机器学习算法提供最优分配建议</p>
                  </div>
                  <Switch
                    checked={config.enableAIRecommendation}
                    onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, enableAIRecommendation: checked }))}
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="constraints" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>资源约束条件</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="maxWorkload">最大工作负载 (%)</Label>
                    <Input
                      id="maxWorkload"
                      type="number"
                      value={config.maxWorkloadPerPerson}
                      onChange={(e) => setConfig((prev) => ({ ...prev, maxWorkloadPerPerson: Number(e.target.value) }))}
                      min={50}
                      max={100}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="skillThreshold">最低技能匹配度 (%)</Label>
                    <Input
                      id="skillThreshold"
                      type="number"
                      value={config.minSkillMatchThreshold}
                      onChange={(e) =>
                        setConfig((prev) => ({ ...prev, minSkillMatchThreshold: Number(e.target.value) }))
                      }
                      min={0}
                      max={100}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <Label>允许加班</Label>
                      <p className="text-xs text-muted-foreground">在紧急情况下允许超出正常工作时间</p>
                    </div>
                    <Switch
                      checked={config.allowOvertime}
                      onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, allowOvertime: checked }))}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <Label>优先考虑经验</Label>
                      <p className="text-xs text-muted-foreground">在技能相同的情况下优先分配经验丰富的人员</p>
                    </div>
                    <Switch
                      checked={config.prioritizeExperience}
                      onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, prioritizeExperience: checked }))}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="time" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>时间配置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-4 md:grid-cols-3">
                  <div className="space-y-2">
                    <Label htmlFor="workingHours">每日工作小时</Label>
                    <Input
                      id="workingHours"
                      type="number"
                      value={config.workingHoursPerDay}
                      onChange={(e) => setConfig((prev) => ({ ...prev, workingHoursPerDay: Number(e.target.value) }))}
                      min={6}
                      max={12}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="workingDays">每周工作天数</Label>
                    <Input
                      id="workingDays"
                      type="number"
                      value={config.workingDaysPerWeek}
                      onChange={(e) => setConfig((prev) => ({ ...prev, workingDaysPerWeek: Number(e.target.value) }))}
                      min={5}
                      max={7}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="bufferTime">项目缓冲时间 (%)</Label>
                    <Input
                      id="bufferTime"
                      type="number"
                      value={config.projectBufferTime}
                      onChange={(e) => setConfig((prev) => ({ ...prev, projectBufferTime: Number(e.target.value) }))}
                      min={0}
                      max={50}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>通知和提醒设置</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <Label>冲突提醒</Label>
                      <p className="text-xs text-muted-foreground">当检测到资源冲突时自动提醒</p>
                    </div>
                    <Switch
                      checked={config.enableConflictAlerts}
                      onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, enableConflictAlerts: checked }))}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="space-y-1">
                      <Label>工作负载警告</Label>
                      <p className="text-xs text-muted-foreground">当人员工作负载过高时发出警告</p>
                    </div>
                    <Switch
                      checked={config.enableWorkloadWarnings}
                      onCheckedChange={(checked) => setConfig((prev) => ({ ...prev, enableWorkloadWarnings: checked }))}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="autoSave">自动保存间隔 (分钟)</Label>
                  <Input
                    id="autoSave"
                    type="number"
                    value={config.autoSaveInterval}
                    onChange={(e) => setConfig((prev) => ({ ...prev, autoSaveInterval: Number(e.target.value) }))}
                    min={1}
                    max={60}
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <div className="flex justify-end space-x-2 pt-4 border-t">
          <Button variant="outline" onClick={handleReset}>
            重置默认
          </Button>
          <Button onClick={handleSave} className="bg-primary hover:bg-primary/90">
            保存配置
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
