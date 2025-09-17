"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Slider } from "@/components/ui/slider"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Settings, Target, Shield, Users, Play, Save } from "lucide-react"
import { mockProjects, type SchedulingConfig } from "@/lib/mock-data"

interface SchedulingConfigProps {
  onExecute: (config: SchedulingConfig) => void
  onSave: (config: SchedulingConfig) => void
}

export function SchedulingConfigForm({ onExecute, onSave }: SchedulingConfigProps) {
  const [config, setConfig] = useState<Partial<SchedulingConfig>>({
    name: "",
    projectIds: [],
    startDate: "",
    endDate: "",
    objectives: {
      efficiency: true,
      costControl: true,
      loadBalancing: true,
      skillMatching: true,
    },
    constraints: {
      skillMatch: true,
      timeConflict: true,
      workloadLimit: true,
      availability: true,
    },
    maxWorkloadPercentage: 85,
    preferredTeamSize: 5,
  })

  const handleProjectToggle = (projectId: string, checked: boolean) => {
    setConfig((prev) => ({
      ...prev,
      projectIds: checked
        ? [...(prev.projectIds || []), projectId]
        : (prev.projectIds || []).filter((id) => id !== projectId),
    }))
  }

  const handleObjectiveChange = (objective: keyof SchedulingConfig["objectives"], checked: boolean) => {
    setConfig((prev) => ({
      ...prev,
      objectives: {
        ...prev.objectives!,
        [objective]: checked,
      },
    }))
  }

  const handleConstraintChange = (constraint: keyof SchedulingConfig["constraints"], checked: boolean) => {
    setConfig((prev) => ({
      ...prev,
      constraints: {
        ...prev.constraints!,
        [constraint]: checked,
      },
    }))
  }

  const handleExecute = () => {
    if (isConfigValid()) {
      onExecute(config as SchedulingConfig)
    }
  }

  const handleSave = () => {
    if (isConfigValid()) {
      onSave(config as SchedulingConfig)
    }
  }

  const isConfigValid = () => {
    return (
      config.name &&
      config.projectIds &&
      config.projectIds.length > 0 &&
      config.startDate &&
      config.endDate &&
      new Date(config.startDate) < new Date(config.endDate)
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-balance">智能调度</h1>
        <p className="text-muted-foreground mt-1">配置调度参数，执行智能人员分配算法</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Basic Configuration */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                基础配置
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">方案名称</Label>
                  <Input
                    id="name"
                    placeholder="输入调度方案名称"
                    value={config.name}
                    onChange={(e) => setConfig((prev) => ({ ...prev, name: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label>调度周期</Label>
                  <div className="flex gap-2">
                    <Input
                      type="date"
                      value={config.startDate}
                      onChange={(e) => setConfig((prev) => ({ ...prev, startDate: e.target.value }))}
                    />
                    <Input
                      type="date"
                      value={config.endDate}
                      onChange={(e) => setConfig((prev) => ({ ...prev, endDate: e.target.value }))}
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <Label>选择项目</Label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {mockProjects.map((project) => (
                    <div key={project.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={`project-${project.id}`}
                        checked={config.projectIds?.includes(project.id)}
                        onCheckedChange={(checked) => handleProjectToggle(project.id, checked as boolean)}
                      />
                      <Label htmlFor={`project-${project.id}`} className="flex-1 cursor-pointer">
                        <div>
                          <div className="font-medium">{project.name}</div>
                          <div className="text-sm text-muted-foreground">{project.description}</div>
                        </div>
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Optimization Objectives */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5" />
                优化目标
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="efficiency"
                    checked={config.objectives?.efficiency}
                    onCheckedChange={(checked) => handleObjectiveChange("efficiency", checked as boolean)}
                  />
                  <Label htmlFor="efficiency" className="cursor-pointer">
                    <div>
                      <div className="font-medium">效率优先</div>
                      <div className="text-sm text-muted-foreground">最大化团队工作效率</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="costControl"
                    checked={config.objectives?.costControl}
                    onCheckedChange={(checked) => handleObjectiveChange("costControl", checked as boolean)}
                  />
                  <Label htmlFor="costControl" className="cursor-pointer">
                    <div>
                      <div className="font-medium">成本控制</div>
                      <div className="text-sm text-muted-foreground">降低人力成本</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="loadBalancing"
                    checked={config.objectives?.loadBalancing}
                    onCheckedChange={(checked) => handleObjectiveChange("loadBalancing", checked as boolean)}
                  />
                  <Label htmlFor="loadBalancing" className="cursor-pointer">
                    <div>
                      <div className="font-medium">负载均衡</div>
                      <div className="text-sm text-muted-foreground">平衡团队工作负载</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="skillMatching"
                    checked={config.objectives?.skillMatching}
                    onCheckedChange={(checked) => handleObjectiveChange("skillMatching", checked as boolean)}
                  />
                  <Label htmlFor="skillMatching" className="cursor-pointer">
                    <div>
                      <div className="font-medium">技能匹配</div>
                      <div className="text-sm text-muted-foreground">优化技能与任务匹配</div>
                    </div>
                  </Label>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Constraints */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="w-5 h-5" />
                约束条件
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="skillMatch"
                    checked={config.constraints?.skillMatch}
                    onCheckedChange={(checked) => handleConstraintChange("skillMatch", checked as boolean)}
                  />
                  <Label htmlFor="skillMatch" className="cursor-pointer">
                    <div>
                      <div className="font-medium">技能匹配</div>
                      <div className="text-sm text-muted-foreground">必须匹配所需技能</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="timeConflict"
                    checked={config.constraints?.timeConflict}
                    onCheckedChange={(checked) => handleConstraintChange("timeConflict", checked as boolean)}
                  />
                  <Label htmlFor="timeConflict" className="cursor-pointer">
                    <div>
                      <div className="font-medium">时间冲突</div>
                      <div className="text-sm text-muted-foreground">避免时间冲突</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="workloadLimit"
                    checked={config.constraints?.workloadLimit}
                    onCheckedChange={(checked) => handleConstraintChange("workloadLimit", checked as boolean)}
                  />
                  <Label htmlFor="workloadLimit" className="cursor-pointer">
                    <div>
                      <div className="font-medium">工作量限制</div>
                      <div className="text-sm text-muted-foreground">限制最大工作负载</div>
                    </div>
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="availability"
                    checked={config.constraints?.availability}
                    onCheckedChange={(checked) => handleConstraintChange("availability", checked as boolean)}
                  />
                  <Label htmlFor="availability" className="cursor-pointer">
                    <div>
                      <div className="font-medium">可用性</div>
                      <div className="text-sm text-muted-foreground">考虑员工可用时间</div>
                    </div>
                  </Label>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Advanced Settings */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                高级设置
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <Label>最大工作负载 ({config.maxWorkloadPercentage}%)</Label>
                <Slider
                  value={[config.maxWorkloadPercentage || 85]}
                  onValueChange={(value) => setConfig((prev) => ({ ...prev, maxWorkloadPercentage: value[0] }))}
                  max={100}
                  min={50}
                  step={5}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>50%</span>
                  <span>100%</span>
                </div>
              </div>

              <Separator />

              <div className="space-y-3">
                <Label>首选团队规模 ({config.preferredTeamSize}人)</Label>
                <Slider
                  value={[config.preferredTeamSize || 5]}
                  onValueChange={(value) => setConfig((prev) => ({ ...prev, preferredTeamSize: value[0] }))}
                  max={20}
                  min={2}
                  step={1}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>2人</span>
                  <span>20人</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Selected Projects Summary */}
          <Card>
            <CardHeader>
              <CardTitle>已选项目</CardTitle>
            </CardHeader>
            <CardContent>
              {config.projectIds && config.projectIds.length > 0 ? (
                <div className="space-y-2">
                  {config.projectIds.map((projectId) => {
                    const project = mockProjects.find((p) => p.id === projectId)
                    return (
                      project && (
                        <div key={projectId} className="flex items-center justify-between p-2 border rounded">
                          <div>
                            <div className="font-medium text-sm">{project.name}</div>
                            <Badge variant="outline" className="text-xs mt-1">
                              {project.status === "active"
                                ? "进行中"
                                : project.status === "planning"
                                  ? "规划中"
                                  : "已完成"}
                            </Badge>
                          </div>
                        </div>
                      )
                    )
                  })}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">请选择要调度的项目</p>
              )}
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="space-y-3">
            <Button onClick={handleExecute} disabled={!isConfigValid()} className="w-full gap-2" size="lg">
              <Play className="w-4 h-4" />
              开始调度
            </Button>
            <Button
              variant="outline"
              onClick={handleSave}
              disabled={!isConfigValid()}
              className="w-full gap-2 bg-transparent"
            >
              <Save className="w-4 h-4" />
              保存方案
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
