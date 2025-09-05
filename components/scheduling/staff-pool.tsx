"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Briefcase } from "lucide-react"

interface Staff {
  id: string
  name: string
  department: string
  position: string
  skills: string[]
  level: string
  workload: number
  availability: string
  hourlyRate: number
}

interface StaffPoolProps {
  staff: Staff[]
  onDragStart: (staff: Staff) => void
  onDragEnd: () => void
}

export function StaffPool({ staff, onDragStart, onDragEnd }: StaffPoolProps) {
  const getAvailabilityColor = (availability: string) => {
    switch (availability) {
      case "可用":
        return "bg-green-100 text-green-800"
      case "忙碌":
        return "bg-yellow-100 text-yellow-800"
      case "不可用":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getWorkloadColor = (workload: number) => {
    if (workload >= 90) return "bg-red-500"
    if (workload >= 70) return "bg-yellow-500"
    return "bg-green-500"
  }

  return (
    <div className="space-y-3 max-h-[600px] overflow-y-auto">
      {staff.map((person) => (
        <Card
          key={person.id}
          className={`cursor-move hover:shadow-md transition-all border-border/50 ${
            person.availability === "可用" ? "hover:border-primary/50" : "opacity-60"
          }`}
          draggable={person.availability === "可用"}
          onDragStart={() => onDragStart(person)}
          onDragEnd={onDragEnd}
        >
          <CardContent className="p-4">
            <div className="flex items-start space-x-3">
              <Avatar className="w-10 h-10">
                <AvatarImage src="/placeholder.svg?height=40&width=40" alt={person.name} />
                <AvatarFallback>{person.name.charAt(0)}</AvatarFallback>
              </Avatar>

              <div className="flex-1 space-y-2">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-sm">{person.name}</h4>
                    <p className="text-xs text-muted-foreground">{person.position}</p>
                  </div>
                  <Badge className={getAvailabilityColor(person.availability)} variant="secondary">
                    {person.availability}
                  </Badge>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1">
                    <Briefcase className="w-3 h-3 text-muted-foreground" />
                    <span className="text-muted-foreground">{person.department}</span>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {person.level}
                  </Badge>
                </div>

                <div className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">工作负载</span>
                    <span>{person.workload}%</span>
                  </div>
                  <Progress value={person.workload} className="h-1.5" />
                </div>

                <div className="flex flex-wrap gap-1">
                  {person.skills.slice(0, 3).map((skill) => (
                    <Badge key={skill} variant="secondary" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                  {person.skills.length > 3 && (
                    <Badge variant="secondary" className="text-xs">
                      +{person.skills.length - 3}
                    </Badge>
                  )}
                </div>

                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">时薪</span>
                  <span className="font-medium">¥{person.hourlyRate}/小时</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
