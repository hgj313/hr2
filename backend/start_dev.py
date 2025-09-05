#!/usr/bin/env python3
"""开发环境启动脚本

本脚本用于快速启动人力资源调度系统的开发环境。
包括数据库初始化、依赖检查和服务启动等功能。
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def check_dependencies():
    """检查依赖是否安装"""
    print("\n📦 Checking dependencies...")
    try:
        import fastapi
        import sqlalchemy
        import redis
        import pydantic
        print("✅ All core dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)


def check_env_file():
    """检查环境变量文件"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("\n📝 Creating .env file from .env.example...")
            env_file.write_text(env_example.read_text(encoding='utf-8'), encoding='utf-8')
            print("✅ .env file created")
            print("⚠️  Please update the .env file with your actual configuration")
        else:
            print("❌ .env.example file not found")
            sys.exit(1)
    else:
        print("✅ .env file exists")


def check_database_connection():
    """检查数据库连接"""
    print("\n🗄️  Checking database connection...")
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and configured correctly")
        return False


def check_redis_connection():
    """检查Redis连接"""
    print("\n🔴 Checking Redis connection...")
    try:
        import redis
        from app.core.config import settings
        
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        print("Please ensure Redis is running")
        return False


def run_migrations():
    """运行数据库迁移"""
    print("\n🔄 Running database migrations...")
    try:
        result = subprocess.run(["alembic", "upgrade", "head"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Database migrations completed")
        else:
            print(f"❌ Migration failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Alembic not found. Please install requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    return True


def create_initial_data():
    """创建初始数据"""
    print("\n👤 Creating initial data...")
    try:
        from app.core.database import SessionLocal
        from app.models.auth import User, Role, Permission
        from app.core.security import get_password_hash
        
        db = SessionLocal()
        
        # 检查是否已有管理员用户
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            # 创建管理员角色
            admin_role = Role(
                name="admin",
                display_name="系统管理员",
                description="系统管理员角色",
                is_system=True
            )
            db.add(admin_role)
            db.flush()
            
            # 创建管理员用户
            admin_user = User(
                email="admin@example.com",
                username="admin",
                full_name="系统管理员",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Initial admin user created (admin@example.com / admin123)")
        else:
            print("✅ Admin user already exists")
        
        db.close()
    except Exception as e:
        print(f"❌ Failed to create initial data: {e}")
        return False
    return True


def start_server():
    """启动开发服务器"""
    print("\n🚀 Starting development server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([
            "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")


def main():
    """主函数"""
    print("🎯 HR Scheduling System - Development Setup")
    print("=" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 检查依赖
    check_dependencies()
    
    # 检查环境文件
    check_env_file()
    
    # 检查数据库连接
    db_ok = check_database_connection()
    
    # 检查Redis连接
    redis_ok = check_redis_connection()
    
    if not db_ok:
        print("\n⚠️  Database connection failed. Please check your configuration.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    if not redis_ok:
        print("\n⚠️  Redis connection failed. Some features may not work properly.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # 运行数据库迁移
    if db_ok:
        if not run_migrations():
            print("\n⚠️  Migration failed. Please check your database configuration.")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
        
        # 创建初始数据
        create_initial_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Quick Start Guide:")
    print("1. Admin login: admin@example.com / admin123")
    print("2. API docs: http://localhost:8000/docs")
    print("3. Health check: http://localhost:8000/health")
    print("\n" + "=" * 50)
    
    # 启动服务器
    start_server()


if __name__ == "__main__":
    main()