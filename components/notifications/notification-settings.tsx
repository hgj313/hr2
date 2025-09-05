"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  Bell,
  Mail,
  MessageSquare,
  Smartphone,
  Settings,
  Volume2,
  VolumeX,
} from "lucide-react"
import {
  useUpdateNotificationSettings,
  type NotificationSettings as NotificationSettingsType,
} from "@/lib/api/notifications"
import { useToast } from "@/components/ui/use-toast"

interface NotificationSettingsProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  settings?: NotificationSettingsType
}

export function NotificationSettings({
  open,
  onOpenChange,
  settings,
}: NotificationSettingsProps) {
  const [localSettings, setLocalSettings] = useState<NotificationSettingsType>({
    emailNotifications: settings?.emailNotifications ?? true,
    pushNotifications: settings?.pushNotifications ?? true,
    smsNotifications: settings?.smsNotifications ?? false,
    soundEnabled: settings?.soundEnabled ?? true,
    notificationFrequency: settings?.notificationFrequency ?? "immediate",
    quietHours: {
      enabled: settings?.quietHours?.enabled ?? false,
      startTime: settings?.quietHours?.startTime ?? "22:00",
      endTime: settings?.quietHours?.endTime ?? "08:00",
    },
    categories: {
      system: settings?.categories?.system ?? true,
      project: settings?.categories?.project ?? true,
      schedule: settings?.categories?.schedule ?? true,
      user: settings?.categories?.user ?? true,
      reminder: settings?.categories?.reminder ?? true,
    },
    priorities: {
      urgent: settings?.priorities?.urgent ?? true,
      high: settings?.priorities?.high ?? true,
      medium: settings?.priorities?.medium ?? true,
      low: settings?.priorities?.low ?? false,
    },
  })

  const { toast } = useToast()
  const updateSettingsMutation = useUpdateNotificationSettings()

  const handleSave = async () => {
    try {
      await updateSettingsMutation.mutateAsync(localSettings)
      toast({
        title: "设置已保存",
        description: "通知设置已成功更新",
      })
      onOpenChange(false)
    } catch (error) {
      toast({
        title: "保存失败",
        description: "更新通知设置时发生错误",
        variant: "destructive",
      })
    }
  }

  const handleReset = () => {
    setLocalSettings({
      emailNotifications: true,
      pushNotifications: true,
      smsNotifications: false,
      soundEnabled: true,
      notificationFrequency: "immediate",
      quietHours: {
        enabled: false,
        startTime: "22:00",
        endTime: "08:00",
      },
      categories: {
        system: true,
        project: true,
        schedule: true,
        user: true,
        reminder: true,
      },
      priorities: {
        urgent: true,
        high: true,
        medium: true,
        low: false,
      },
    })
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            通知设置
          </DialogTitle>
          <DialogDescription>
            自定义您的通知偏好设置
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {/* 通知方式 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">通知方式</CardTitle>
              <CardDescription>
                选择您希望接收通知的方式
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  <Label htmlFor="email-notifications">邮件通知</Label>
                </div>
                <Switch
                  id="email-notifications"
                  checked={localSettings.emailNotifications}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({ ...prev, emailNotifications: checked }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Bell className="h-4 w-4 text-muted-foreground" />
                  <Label htmlFor="push-notifications">推送通知</Label>
                </div>
                <Switch
                  id="push-notifications"
                  checked={localSettings.pushNotifications}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({ ...prev, pushNotifications: checked }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Smartphone className="h-4 w-4 text-muted-foreground" />
                  <Label htmlFor="sms-notifications">短信通知</Label>
                </div>
                <Switch
                  id="sms-notifications"
                  checked={localSettings.smsNotifications}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({ ...prev, smsNotifications: checked }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {localSettings.soundEnabled ? (
                    <Volume2 className="h-4 w-4 text-muted-foreground" />
                  ) : (
                    <VolumeX className="h-4 w-4 text-muted-foreground" />
                  )}
                  <Label htmlFor="sound-enabled">声音提醒</Label>
                </div>
                <Switch
                  id="sound-enabled"
                  checked={localSettings.soundEnabled}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({ ...prev, soundEnabled: checked }))
                  }
                />
              </div>
            </CardContent>
          </Card>

          {/* 通知频率 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">通知频率</CardTitle>
              <CardDescription>
                设置接收通知的频率
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Select
                value={localSettings.notificationFrequency}
                onValueChange={(value) =>
                  setLocalSettings(prev => ({ ...prev, notificationFrequency: value as any }))
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="immediate">立即通知</SelectItem>
                  <SelectItem value="hourly">每小时汇总</SelectItem>
                  <SelectItem value="daily">每日汇总</SelectItem>
                  <SelectItem value="weekly">每周汇总</SelectItem>
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          {/* 免打扰时间 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">免打扰时间</CardTitle>
              <CardDescription>
                设置不接收通知的时间段
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <Label htmlFor="quiet-hours-enabled">启用免打扰</Label>
                <Switch
                  id="quiet-hours-enabled"
                  checked={localSettings.quietHours.enabled}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      quietHours: { ...prev.quietHours, enabled: checked }
                    }))
                  }
                />
              </div>
              
              {localSettings.quietHours.enabled && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="start-time">开始时间</Label>
                    <Select
                      value={localSettings.quietHours.startTime}
                      onValueChange={(value) =>
                        setLocalSettings(prev => ({
                          ...prev,
                          quietHours: { ...prev.quietHours, startTime: value }
                        }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {Array.from({ length: 24 }, (_, i) => {
                          const hour = i.toString().padStart(2, '0')
                          return (
                            <SelectItem key={hour} value={`${hour}:00`}>
                              {hour}:00
                            </SelectItem>
                          )
                        })}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <Label htmlFor="end-time">结束时间</Label>
                    <Select
                      value={localSettings.quietHours.endTime}
                      onValueChange={(value) =>
                        setLocalSettings(prev => ({
                          ...prev,
                          quietHours: { ...prev.quietHours, endTime: value }
                        }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {Array.from({ length: 24 }, (_, i) => {
                          const hour = i.toString().padStart(2, '0')
                          return (
                            <SelectItem key={hour} value={`${hour}:00`}>
                              {hour}:00
                            </SelectItem>
                          )
                        })}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* 通知类别 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">通知类别</CardTitle>
              <CardDescription>
                选择您希望接收的通知类别
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <Label htmlFor="system-notifications">系统通知</Label>
                <Switch
                  id="system-notifications"
                  checked={localSettings.categories.system}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      categories: { ...prev.categories, system: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="project-notifications">项目通知</Label>
                <Switch
                  id="project-notifications"
                  checked={localSettings.categories.project}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      categories: { ...prev.categories, project: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="schedule-notifications">调度通知</Label>
                <Switch
                  id="schedule-notifications"
                  checked={localSettings.categories.schedule}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      categories: { ...prev.categories, schedule: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="user-notifications">用户通知</Label>
                <Switch
                  id="user-notifications"
                  checked={localSettings.categories.user}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      categories: { ...prev.categories, user: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="reminder-notifications">提醒通知</Label>
                <Switch
                  id="reminder-notifications"
                  checked={localSettings.categories.reminder}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      categories: { ...prev.categories, reminder: checked }
                    }))
                  }
                />
              </div>
            </CardContent>
          </Card>

          {/* 优先级设置 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">优先级设置</CardTitle>
              <CardDescription>
                选择您希望接收的通知优先级
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <Label htmlFor="urgent-notifications">紧急通知</Label>
                <Switch
                  id="urgent-notifications"
                  checked={localSettings.priorities.urgent}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      priorities: { ...prev.priorities, urgent: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="high-notifications">高优先级通知</Label>
                <Switch
                  id="high-notifications"
                  checked={localSettings.priorities.high}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      priorities: { ...prev.priorities, high: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="medium-notifications">中优先级通知</Label>
                <Switch
                  id="medium-notifications"
                  checked={localSettings.priorities.medium}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      priorities: { ...prev.priorities, medium: checked }
                    }))
                  }
                />
              </div>
              
              <div className="flex items-center justify-between">
                <Label htmlFor="low-notifications">低优先级通知</Label>
                <Switch
                  id="low-notifications"
                  checked={localSettings.priorities.low}
                  onCheckedChange={(checked) =>
                    setLocalSettings(prev => ({
                      ...prev,
                      priorities: { ...prev.priorities, low: checked }
                    }))
                  }
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={handleReset}>
            重置默认
          </Button>
          <Button onClick={handleSave} disabled={updateSettingsMutation.isPending}>
            {updateSettingsMutation.isPending ? "保存中..." : "保存设置"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}