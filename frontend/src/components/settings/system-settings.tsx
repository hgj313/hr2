"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Settings, Users, Shield, Database, Bell, Globe, Clock } from "lucide-react"

interface SystemConfig {
  companyName: string
  timezone: string
  language: string
  theme: string
  workingHours: {
    start: string
    end: string
  }
  notifications: {
    email: boolean
    sms: boolean
    push: boolean
  }
  security: {
    passwordPolicy: string
    sessionTimeout: number
    twoFactorAuth: boolean
  }
  integrations: {
    email: boolean
    calendar: boolean
    hrms: boolean
    payroll: boolean
  }
}

const mockSystemConfig: SystemConfig = {
  companyName: "科技创新有限公司",
  timezone: "Asia/Shanghai",
  language: "zh-CN",
  theme: "light",
  workingHours: {
    start: "09:00",
    end: "18:00",
  },
  notifications: {
    email: true,
    sms: false,
    push: true,
  },
  security: {
    passwordPolicy: "strong",
    sessionTimeout: 30,
    twoFactorAuth: false,
  },
  integrations: {
    email: true,
    calendar: true,
    hrms: false,
    payroll: false,
  },
}

export function SystemSettings() {
  const [config, setConfig] = useState<SystemConfig>(mockSystemConfig)
  const [activeTab, setActiveTab] = useState("general")

  const handleSave = () => {
    console.log("保存系统配置:", config)
    // TODO: 实际保存配置到后端
  }

  const updateConfig = (section: keyof SystemConfig, key: string, value: any) => {
    setConfig((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value,
      },
    }))
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">系统设置</h1>
          <p className="text-muted-foreground">管理系统配置和集成设置</p>
        </div>
        <Button onClick={handleSave} className="bg-primary hover:bg-primary/90">
          <Settings className="w-4 h-4 mr-2" />
          保存设置
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="general" className="flex items-center gap-2">
            <Globe className="w-4 h-4" />
            基本设置
          </TabsTrigger>
          <TabsTrigger value="users" className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            用户管理
          </TabsTrigger>
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            安全设置
          </TabsTrigger>
          <TabsTrigger value="notifications" className="flex items-center gap-2">
            <Bell className="w-4 h-4" />
            通知设置
          </TabsTrigger>
          <TabsTrigger value="integrations" className="flex items-center gap-2">
            <Database className="w-4 h-4" />
            系统集成
          </TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="w-5 h-5" />
                基本信息
              </CardTitle>
              <CardDescription>配置公司基本信息和系统参数</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="companyName">公司名称</Label>
                  <Input
                    id="companyName"
                    value={config.companyName}
                    onChange={(e) => setConfig((prev) => ({ ...prev, companyName: e.target.value }))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="timezone">时区</Label>
                  <Select
                    value={config.timezone}
                    onValueChange={(value) => setConfig((prev) => ({ ...prev, timezone: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Asia/Shanghai">中国标准时间 (UTC+8)</SelectItem>
                      <SelectItem value="Asia/Tokyo">日本标准时间 (UTC+9)</SelectItem>
                      <SelectItem value="America/New_York">美国东部时间 (UTC-5)</SelectItem>
                      <SelectItem value="Europe/London">格林威治时间 (UTC+0)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="language">系统语言</Label>
                  <Select
                    value={config.language}
                    onValueChange={(value) => setConfig((prev) => ({ ...prev, language: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="zh-CN">简体中文</SelectItem>
                      <SelectItem value="zh-TW">繁体中文</SelectItem>
                      <SelectItem value="en-US">English</SelectItem>
                      <SelectItem value="ja-JP">日本語</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="theme">界面主题</Label>
                  <Select
                    value={config.theme}
                    onValueChange={(value) => setConfig((prev) => ({ ...prev, theme: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="light">浅色主题</SelectItem>
                      <SelectItem value="dark">深色主题</SelectItem>
                      <SelectItem value="auto">跟随系统</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Separator />

              <div>
                <Label className="text-base font-medium flex items-center gap-2 mb-4">
                  <Clock className="w-4 h-4" />
                  工作时间设置
                </Label>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="startTime">开始时间</Label>
                    <Input
                      id="startTime"
                      type="time"
                      value={config.workingHours.start}
                      onChange={(e) => updateConfig("workingHours", "start", e.target.value)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="endTime">结束时间</Label>
                    <Input
                      id="endTime"
                      type="time"
                      value={config.workingHours.end}
                      onChange={(e) => updateConfig("workingHours", "end", e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="users" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                用户权限管理
              </CardTitle>
              <CardDescription>管理用户角色和权限设置</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { role: "系统管理员", users: 2, permissions: ["全部权限"], color: "bg-red-100 text-red-800" },
                  {
                    role: "HR经理",
                    users: 5,
                    permissions: ["人员管理", "项目管理", "调度管理"],
                    color: "bg-blue-100 text-blue-800",
                  },
                  {
                    role: "项目经理",
                    users: 12,
                    permissions: ["项目管理", "团队管理"],
                    color: "bg-green-100 text-green-800",
                  },
                  {
                    role: "部门主管",
                    users: 8,
                    permissions: ["部门人员查看", "调度查看"],
                    color: "bg-yellow-100 text-yellow-800",
                  },
                  { role: "普通员工", users: 156, permissions: ["个人信息查看"], color: "bg-gray-100 text-gray-800" },
                ].map((role, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <Badge className={role.color}>{role.role}</Badge>
                      <div>
                        <p className="font-medium">{role.users} 位用户</p>
                        <p className="text-sm text-muted-foreground">权限: {role.permissions.join(", ")}</p>
                      </div>
                    </div>
                    <Button variant="outline" size="sm">
                      编辑权限
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="w-5 h-5" />
                安全策略
              </CardTitle>
              <CardDescription>配置系统安全和访问控制策略</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="passwordPolicy">密码策略</Label>
                  <Select
                    value={config.security.passwordPolicy}
                    onValueChange={(value) => updateConfig("security", "passwordPolicy", value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="basic">基础 (6位以上)</SelectItem>
                      <SelectItem value="medium">中等 (8位，包含字母数字)</SelectItem>
                      <SelectItem value="strong">强密码 (8位，包含大小写字母、数字、特殊字符)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sessionTimeout">会话超时 (分钟)</Label>
                  <Input
                    id="sessionTimeout"
                    type="number"
                    value={config.security.sessionTimeout}
                    onChange={(e) => updateConfig("security", "sessionTimeout", Number.parseInt(e.target.value))}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">双因素认证</Label>
                    <p className="text-sm text-muted-foreground">启用双因素认证以提高账户安全性</p>
                  </div>
                  <Switch
                    checked={config.security.twoFactorAuth}
                    onCheckedChange={(checked) => updateConfig("security", "twoFactorAuth", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="w-5 h-5" />
                通知设置
              </CardTitle>
              <CardDescription>配置系统通知和提醒方式</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">邮件通知</Label>
                    <p className="text-sm text-muted-foreground">通过邮件发送重要通知和提醒</p>
                  </div>
                  <Switch
                    checked={config.notifications.email}
                    onCheckedChange={(checked) => updateConfig("notifications", "email", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">短信通知</Label>
                    <p className="text-sm text-muted-foreground">通过短信发送紧急通知</p>
                  </div>
                  <Switch
                    checked={config.notifications.sms}
                    onCheckedChange={(checked) => updateConfig("notifications", "sms", checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">推送通知</Label>
                    <p className="text-sm text-muted-foreground">通过浏览器推送实时通知</p>
                  </div>
                  <Switch
                    checked={config.notifications.push}
                    onCheckedChange={(checked) => updateConfig("notifications", "push", checked)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="w-5 h-5" />
                系统集成
              </CardTitle>
              <CardDescription>管理与第三方系统的集成配置</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid gap-4">
                {[
                  {
                    name: "邮件系统",
                    description: "集成企业邮箱系统，支持邮件通知发送",
                    status: config.integrations.email,
                    key: "email",
                  },
                  {
                    name: "日历系统",
                    description: "同步企业日历，支持会议和日程安排",
                    status: config.integrations.calendar,
                    key: "calendar",
                  },
                  {
                    name: "HRMS系统",
                    description: "集成现有人力资源管理系统",
                    status: config.integrations.hrms,
                    key: "hrms",
                  },
                  {
                    name: "薪资系统",
                    description: "集成薪资管理系统，支持工时统计",
                    status: config.integrations.payroll,
                    key: "payroll",
                  },
                ].map((integration, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className={`w-3 h-3 rounded-full ${integration.status ? "bg-green-500" : "bg-gray-300"}`} />
                      <div>
                        <p className="font-medium">{integration.name}</p>
                        <p className="text-sm text-muted-foreground">{integration.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={integration.status ? "default" : "secondary"}>
                        {integration.status ? "已连接" : "未连接"}
                      </Badge>
                      <Switch
                        checked={integration.status}
                        onCheckedChange={(checked) => updateConfig("integrations", integration.key, checked)}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
