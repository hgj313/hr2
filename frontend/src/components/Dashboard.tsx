import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import {
  UsersIcon,
  BriefcaseIcon,
  ClockIcon,
  ChartBarIcon,
  CalendarDaysIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';
import '../styles/chinese-minimal.css';

interface DashboardStats {
  total_users: number;
  active_projects: number;
  total_assignments: number;
  pending_tasks: number;
}

interface RecentActivity {
  id: number;
  type: string;
  description: string;
  timestamp: string;
  user?: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    total_users: 0,
    active_projects: 0,
    total_assignments: 0,
    pending_tasks: 0,
  });
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // 获取统计数据
      const [usersResponse, projectsResponse] = await Promise.all([
        axios.get('/api/v1/users/'),
        axios.get('/api/v1/projects/'),
      ]);
      
      const users = usersResponse.data;
      const projects = projectsResponse.data;
      
      setStats({
        total_users: users.length,
        active_projects: projects.filter((p: any) => p.status === 'active').length,
        total_assignments: projects.reduce((sum: number, p: any) => sum + (p.assignments?.length || 0), 0),
        pending_tasks: projects.reduce((sum: number, p: any) => sum + (p.pending_tasks || 0), 0),
      });
      
      // 模拟最近活动数据
      setRecentActivities([
        {
          id: 1,
          type: 'project_created',
          description: '新建项目：移动应用开发',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          user: 'admin',
        },
        {
          id: 2,
          type: 'user_assigned',
          description: '张三被分配到Web开发项目',
          timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
          user: 'admin',
        },
        {
          id: 3,
          type: 'task_completed',
          description: '完成任务：数据库设计',
          timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
          user: '李四',
        },
      ]);
      
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setError('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInHours = Math.floor((now.getTime() - time.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return '刚刚';
    if (diffInHours < 24) return `${diffInHours}小时前`;
    return `${Math.floor(diffInHours / 24)}天前`;
  };

  const statCards = [
    {
      name: '总用户数',
      value: stats.total_users,
      icon: UsersIcon,
      color: 'bg-blue-500',
      href: '/users',
    },
    {
      name: '活跃项目',
      value: stats.active_projects,
      icon: BriefcaseIcon,
      color: 'bg-green-500',
      href: '/timeline',
    },
    {
      name: '总分配数',
      value: stats.total_assignments,
      icon: ClockIcon,
      color: 'bg-yellow-500',
      href: '/timeline',
    },
    {
      name: '待处理任务',
      value: stats.pending_tasks,
      icon: ExclamationTriangleIcon,
      color: 'bg-red-500',
      href: '/timeline',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2" style={{borderColor: 'var(--bamboo-medium)'}}></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="pb-4" style={{borderBottom: '1px solid var(--bamboo-light)'}}>
        <h1 style={{fontSize: '1.875rem', fontWeight: '700', color: 'var(--ink-dark)'}} className="seal-accent">仪表板</h1>
        <p style={{marginTop: '0.25rem', fontSize: '0.875rem', color: 'var(--ink-medium)'}}>
          欢迎回来！这里是您的系统概览。
        </p>
      </div>

      {error && (
        <div className="card-minimal" style={{background: 'var(--error-light)', border: '1px solid var(--error-medium)', color: 'var(--error-dark)', padding: '1rem', borderRadius: '0.5rem'}}>
          {error}
        </div>
      )}

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => {
          const Icon = card.icon;
          return (
            <Link
              key={card.name}
              to={card.href}
              className="card-minimal overflow-hidden transition-all duration-300 hover:scale-105 animate-fade-in-up"
              style={{background: 'var(--rice-white)', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', borderRadius: '0.75rem'}}
            >
              <div style={{padding: '1.25rem'}}>
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="seal-accent" style={{background: 'var(--bamboo-medium)', borderRadius: '0.5rem', padding: '0.75rem'}}>
                      <Icon style={{width: '1.5rem', height: '1.5rem', color: 'var(--rice-white)'}} />
                    </div>
                  </div>
                  <div style={{marginLeft: '1.25rem', flex: '1', minWidth: '0'}}>
                    <dl>
                      <dt style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-medium)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>
                        {card.name}
                      </dt>
                      <dd style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)', marginTop: '0.25rem'}}>
                        {card.value}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 最近活动 */}
        <div className="card-minimal animate-fade-in-up" style={{background: 'var(--rice-white)', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', borderRadius: '0.75rem'}}>
          <div style={{padding: '1.5rem'}}>
            <h3 style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)', marginBottom: '1rem'}} className="seal-accent">
              最近活动
            </h3>
            <div className="flow-root">
              <ul style={{marginBottom: '-2rem'}}>
                {recentActivities.map((activity, index) => (
                  <li key={activity.id}>
                    <div className="relative" style={{paddingBottom: '2rem'}}>
                      {index !== recentActivities.length - 1 && (
                        <span
                          className="absolute"
                          style={{top: '1rem', left: '1rem', marginLeft: '-1px', height: '100%', width: '2px', background: 'var(--bamboo-light)'}}
                          aria-hidden="true"
                        />
                      )}
                      <div className="relative flex" style={{gap: '0.75rem'}}>
                        <div>
                          <span className="seal-accent flex items-center justify-center" style={{height: '2rem', width: '2rem', borderRadius: '50%', background: 'var(--bamboo-medium)', border: '4px solid var(--rice-white)'}}>
                            <CheckCircleIcon style={{width: '1rem', height: '1rem', color: 'var(--rice-white)'}} />
                          </span>
                        </div>
                        <div className="min-w-0 flex-1 flex justify-between" style={{paddingTop: '0.375rem', gap: '1rem'}}>
                          <div>
                            <p style={{fontSize: '0.875rem', color: 'var(--ink-dark)'}}>
                              {activity.description}
                            </p>
                            {activity.user && (
                              <p style={{fontSize: '0.75rem', color: 'var(--ink-light)', marginTop: '0.25rem'}}>
                                操作者: {activity.user}
                              </p>
                            )}
                          </div>
                          <div style={{textAlign: 'right', fontSize: '0.75rem', whiteSpace: 'nowrap', color: 'var(--ink-light)'}}>
                            {formatTimeAgo(activity.timestamp)}
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* 快速操作 */}
        <div className="card-minimal animate-fade-in-up" style={{background: 'var(--rice-white)', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', borderRadius: '0.75rem'}}>
          <div style={{padding: '1.5rem'}}>
            <h3 style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)', marginBottom: '1rem'}} className="seal-accent">
              快速操作
            </h3>
            <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
              <Link
                to="/timeline"
                className="w-full flex items-center justify-between transition-all duration-200 hover:scale-105"
                style={{padding: '0.75rem', border: '1px solid var(--bamboo-light)', borderRadius: '0.5rem', background: 'var(--rice-cream)'}}
              >
                <div className="flex items-center">
                  <CalendarDaysIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-medium)', marginRight: '0.75rem'}} />
                  <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>
                    查看项目时间轴
                  </span>
                </div>
                <svg style={{width: '1rem', height: '1rem', color: 'var(--ink-light)'}} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
              
              <Link
                to="/users"
                className="w-full flex items-center justify-between transition-all duration-200 hover:scale-105"
                style={{padding: '0.75rem', border: '1px solid var(--bamboo-light)', borderRadius: '0.5rem', background: 'var(--rice-cream)'}}
              >
                <div className="flex items-center">
                  <UsersIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-medium)', marginRight: '0.75rem'}} />
                  <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>
                    管理用户
                  </span>
                </div>
                <svg style={{width: '1rem', height: '1rem', color: 'var(--ink-light)'}} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
              
              <button
                onClick={fetchDashboardData}
                className="w-full flex items-center justify-between transition-all duration-200 hover:scale-105"
                style={{padding: '0.75rem', border: '1px solid var(--bamboo-light)', borderRadius: '0.5rem', background: 'var(--rice-cream)'}}
              >
                <div className="flex items-center">
                  <ChartBarIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-medium)', marginRight: '0.75rem'}} />
                  <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>
                    刷新数据
                  </span>
                </div>
                <svg style={{width: '1rem', height: '1rem', color: 'var(--ink-light)'}} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;