"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

interface User {
  id: string
  name: string
  email: string
  department: string
  position: string
  skills: string[]
  level: string
  status: string
  avatar: string
  workload: number
}

interface UserCardProps {
  user: User
  onClick?: () => void
}

export function UserCard({ user, onClick }: UserCardProps) {
  const getWorkloadColor = (workload: number) => {
    if (workload >= 90) return "bg-red-500"
    if (workload >= 70) return "bg-yellow-500"
    return "bg-green-500"
  }

  return (
    <Card className="border-border/50 hover:shadow-md transition-shadow cursor-pointer" onClick={onClick}>
      <CardHeader className="pb-3">
        <div className="flex items-center space-x-3">
          <Avatar className="h-10 w-10">
            <AvatarImage src={user.avatar || "/placeholder.svg"} alt={user.name} />
            <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle className="text-base">{user.name}</CardTitle>
            <p className="text-sm text-muted-foreground">{user.position}</p>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">部门:</span>
          <span>{user.department}</span>
        </div>

        <div className="flex items-center justify-between text-sm">
          <span className="text-muted-foreground">级别:</span>
          <Badge variant="outline">{user.level}</Badge>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">工作负载:</span>
            <span>{user.workload}%</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div
              className={`h-2 rounded-full ${getWorkloadColor(user.workload)}`}
              style={{ width: `${user.workload}%` }}
            />
          </div>
        </div>

        <div className="space-y-2">
          <span className="text-sm text-muted-foreground">技能:</span>
          <div className="flex flex-wrap gap-1">
            {user.skills.slice(0, 3).map((skill) => (
              <Badge key={skill} variant="secondary" className="text-xs">
                {skill}
              </Badge>
            ))}
            {user.skills.length > 3 && (
              <Badge variant="secondary" className="text-xs">
                +{user.skills.length - 3}
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
