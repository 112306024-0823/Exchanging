# 交換資訊整理系統 - 開發環境設置

## 專案概述
政大商學院院級交換資訊整合平台，提供學校資訊查詢、心得分享、用戶互動等功能。

## 技術棧
- **前端**: Vue 3 + TypeScript + Vite
- **UI 框架**: Element Plus + Tailwind CSS
- **後端**: Supabase (PostgreSQL + Auth + Realtime)
- **部署**: Vercel/Netlify + Supabase

## 開發環境設置

### 前置需求
- Node.js 18+ 
- npm 或 yarn
- Git
- Supabase CLI (可選)

### 專案初始化
```bash
# 克隆專案
git clone [repository-url]
cd exchange-info-system

# 安裝依賴
npm install

# 設置環境變數
cp .env.example .env.local
```

### 環境變數配置
```env
# Supabase 配置
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

# Google OAuth
VITE_GOOGLE_CLIENT_ID=your_google_client_id

# 地圖 API
VITE_MAP_API_KEY=your_map_api_key
```

## 開發指令

### 開發伺服器
```bash
# 啟動開發伺服器
npm run dev

# 啟動開發伺服器 (指定端口)
npm run dev -- --port 3000
```

### 建置與部署
```bash
# 建置生產版本
npm run build

# 預覽建置結果
npm run preview

# 部署到 Vercel
npm run deploy
```

### 測試
```bash
# 執行單元測試
npm run test

# 執行端到端測試
npm run test:e2e

# 測試覆蓋率報告
npm run test:coverage
```

### 程式碼品質
```bash
# ESLint 檢查
npm run lint

# Prettier 格式化
npm run format

# 類型檢查
npm run type-check
```

## 資料庫設置

### Supabase 專案設置
1. 在 Supabase 控制台創建新專案
2. 設置資料庫表結構
3. 配置 Row Level Security (RLS)
4. 設置認證提供者 (Google OAuth)

### 主要資料表
```sql
-- 學校資料表
CREATE TABLE schools (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  country VARCHAR(100),
  description TEXT,
  courses_offered TEXT[],
  living_cost INTEGER,
  accommodation_info TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用戶資料表
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 心得資料表
CREATE TABLE experiences (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  school_id INTEGER REFERENCES schools(id),
  content TEXT NOT NULL,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 評論資料表
CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  experience_id INTEGER REFERENCES experiences(id),
  user_id INTEGER REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 功能模組開發

### 1. 學校資料管理
- 位置: `src/views/Schools/`
- 主要組件: `SchoolList.vue`, `SchoolDetail.vue`, `SchoolMap.vue`
- API: `src/api/schools.ts`

### 2. 心得管理
- 位置: `src/views/Experiences/`
- 主要組件: `ExperienceList.vue`, `ExperienceDetail.vue`, `ExperienceForm.vue`
- API: `src/api/experiences.ts`

### 3. 用戶系統
- 位置: `src/views/Auth/`
- 主要組件: `Login.vue`, `Profile.vue`
- API: `src/api/auth.ts`

### 4. 投稿系統
- 位置: `src/views/Submission/`
- 主要組件: `SubmissionForm.vue`, `SubmissionReview.vue`
- API: `src/api/submissions.ts`

## 開發最佳實踐

### Vue 組件開發
- 使用 Composition API 和 `<script setup>`
- 實作適當的 props 驗證
- 使用 TypeScript 類型定義
- 遵循單一職責原則

### 狀態管理
- 使用 Pinia 進行全域狀態管理
- 實作適當的狀態持久化
- 使用 computed 和 watch 優化效能

### 樣式開發
- 優先使用 Tailwind CSS 工具類
- 複雜樣式使用 SCSS 模組
- 實作響應式設計
- 支援深色模式

### API 整合
- 使用 Supabase Client
- 實作適當的錯誤處理
- 使用 TypeScript 類型定義
- 實作資料快取

## 測試策略

### 單元測試
- 使用 Vitest 框架
- 測試組件邏輯和 API 函數
- 實作測試覆蓋率目標 80%+

### 整合測試
- 測試組件間互動
- 測試 API 整合
- 測試路由導航

### 端到端測試
- 使用 Playwright
- 測試關鍵用戶流程
- 測試跨瀏覽器相容性

## 部署流程

### 開發環境
- 使用 Vite 開發伺服器
- 熱重載和快速建置
- 開發工具整合

### 測試環境
- 自動化測試執行
- 程式碼品質檢查
- 效能監控

### 生產環境
- 程式碼最小化
- 資源優化
- CDN 配置
- 監控和日誌

## 常見問題

### 開發相關
Q: 如何設置 Supabase 本地開發環境？
A: 使用 Supabase CLI 創建本地實例，或使用 Supabase 雲端服務。

Q: 如何處理 CORS 問題？
A: 在 Supabase 控制台設置允許的域名，或使用代理配置。

### 部署相關
Q: 如何設置環境變數？
A: 在部署平台設置環境變數，確保與本地開發環境一致。

Q: 如何處理資料庫遷移？
A: 使用 Supabase 的遷移功能，或手動執行 SQL 腳本。

## 貢獻指南

### 程式碼提交
- 使用清晰的 commit 訊息
- 遵循 Git Flow 工作流程
- 實作程式碼審查

### 功能開發
- 創建功能分支
- 撰寫測試案例
- 更新文件

### 問題回報
- 使用 GitHub Issues
- 提供詳細的問題描述
- 包含重現步驟 