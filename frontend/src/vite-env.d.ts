/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
  readonly VITE_NODE_ENV: string
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_VERSION: string
  // 添加更多环境变量类型定义...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}