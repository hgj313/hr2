import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const activities = [
  {
    id: 1,
    user: "张三",
    action: "被分配到项目",
    target: "Web开发项目",
    time: "2分钟前",
    avatar: "张",
  },
  {
    id: 2,
    user: "李四",
    action: "完成了任务",
    target: "UI设计评审",
    time: "15分钟前",
    avatar: "李",
  },
  {
    id: 3,
    user: "王五",
    action: "创建了新项目",
    target: "移动应用开发",
    time: "1小时前",
    avatar: "王",
  },
  {
    id: 4,
    user: "赵六",
    action: "更新了进度",
    target: "数据库优化",
    time: "2小时前",
    avatar: "赵",
  },
]

export function RecentActivities() {
  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle>最近活动</CardTitle>
        <CardDescription>团队成员的最新动态</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-center space-x-4">
              <Avatar className="h-8 w-8">
                <AvatarImage src={`/placeholder-32px.png?height=32&width=32`} />
                <AvatarFallback className="text-xs">{activity.avatar}</AvatarFallback>
              </Avatar>
              <div className="flex-1 space-y-1">
                <p className="text-sm">
                  <span className="font-medium">{activity.user}</span>
                  <span className="text-muted-foreground"> {activity.action} </span>
                  <span className="font-medium">{activity.target}</span>
                </p>
                <p className="text-xs text-muted-foreground">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
