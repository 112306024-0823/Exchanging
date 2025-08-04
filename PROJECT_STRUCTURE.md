# 專案結構說明

## 目錄結構
```
exchange-info-system/
├── .cursorrules                 # Cursor 專案規則
├── .cursoruserrules            # Cursor 用戶規則
├── .env.example                # 環境變數範例
├── .gitignore                  # Git 忽略檔案
├── package.json                # 專案依賴
├── vite.config.ts              # Vite 配置
├── tsconfig.json               # TypeScript 配置
├── tailwind.config.js          # Tailwind CSS 配置
├── index.html                  # HTML 入口檔案
├── README.md                   # 專案說明
├── DEVELOPMENT.md              # 開發指南
├── PROJECT_STRUCTURE.md        # 專案結構說明
│
├── public/                     # 靜態資源
│   ├── favicon.ico
│   ├── logo.png
│   └── images/
│
├── src/                        # 原始碼
│   ├── main.ts                 # 應用程式入口
│   ├── App.vue                 # 根組件
│   ├── env.d.ts                # 環境變數類型定義
│   │
│   ├── assets/                 # 資源檔案
│   │   ├── styles/
│   │   │   ├── main.scss       # 主要樣式
│   │   │   ├── variables.scss  # SCSS 變數
│   │   │   └── components.scss # 組件樣式
│   │   ├── images/             # 圖片資源
│   │   └── icons/              # 圖示資源
│   │
│   ├── components/             # 共用組件
│   │   ├── common/             # 通用組件
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseInput.vue
│   │   │   ├── BaseModal.vue
│   │   │   └── BaseLoading.vue
│   │   ├── layout/             # 佈局組件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppFooter.vue
│   │   │   └── AppNavigation.vue
│   │   └── ui/                 # UI 組件
│   │       ├── SchoolCard.vue
│   │       ├── ExperienceCard.vue
│   │       ├── TagList.vue
│   │       └── SearchBar.vue
│   │
│   ├── views/                  # 頁面組件
│   │   ├── Home/               # 首頁
│   │   │   ├── HomePage.vue
│   │   │   └── components/
│   │   │       ├── HeroSection.vue
│   │   │       └── StatsSection.vue
│   │   │
│   │   ├── Schools/            # 學校相關頁面
│   │   │   ├── SchoolListPage.vue
│   │   │   ├── SchoolDetailPage.vue
│   │   │   ├── SchoolMapPage.vue
│   │   │   └── components/
│   │   │       ├── SchoolFilter.vue
│   │   │       ├── SchoolSearch.vue
│   │   │       └── SchoolMap.vue
│   │   │
│   │   ├── Experiences/        # 心得相關頁面
│   │   │   ├── ExperienceListPage.vue
│   │   │   ├── ExperienceDetailPage.vue
│   │   │   ├── ExperienceFormPage.vue
│   │   │   └── components/
│   │   │       ├── ExperienceFilter.vue
│   │   │       ├── ExperienceSearch.vue
│   │   │       └── ExperienceEditor.vue
│   │   │
│   │   ├── Auth/               # 認證相關頁面
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── ProfilePage.vue
│   │   │   └── components/
│   │   │       ├── LoginForm.vue
│   │   │       └── ProfileForm.vue
│   │   │
│   │   ├── Submission/         # 投稿相關頁面
│   │   │   ├── SubmissionFormPage.vue
│   │   │   ├── SubmissionReviewPage.vue
│   │   │   └── components/
│   │   │       ├── SubmissionForm.vue
│   │   │       └── ReviewPanel.vue
│   │   │
│   │   └── Admin/              # 管理相關頁面
│   │       ├── AdminDashboard.vue
│   │       ├── UserManagement.vue
│   │       └── ContentModeration.vue
│   │
│   ├── router/                 # 路由配置
│   │   ├── index.ts            # 路由主檔案
│   │   ├── routes.ts           # 路由定義
│   │   └── guards.ts           # 路由守衛
│   │
│   ├── stores/                 # 狀態管理 (Pinia)
│   │   ├── index.ts            # Store 入口
│   │   ├── auth.ts             # 認證狀態
│   │   ├── schools.ts          # 學校資料狀態
│   │   ├── experiences.ts      # 心得資料狀態
│   │   └── ui.ts               # UI 狀態
│   │
│   ├── api/                    # API 整合
│   │   ├── client.ts           # Supabase 客戶端
│   │   ├── auth.ts             # 認證 API
│   │   ├── schools.ts          # 學校 API
│   │   ├── experiences.ts      # 心得 API
│   │   ├── users.ts            # 用戶 API
│   │   └── submissions.ts      # 投稿 API
│   │
│   ├── types/                  # TypeScript 類型定義
│   │   ├── index.ts            # 類型匯出
│   │   ├── auth.ts             # 認證相關類型
│   │   ├── school.ts           # 學校相關類型
│   │   ├── experience.ts       # 心得相關類型
│   │   ├── user.ts             # 用戶相關類型
│   │   └── api.ts              # API 回應類型
│   │
│   ├── utils/                  # 工具函數
│   │   ├── constants.ts        # 常數定義
│   │   ├── helpers.ts          # 輔助函數
│   │   ├── validators.ts       # 驗證函數
│   │   ├── formatters.ts       # 格式化函數
│   │   └── storage.ts          # 本地儲存
│   │
│   ├── composables/            # Vue 組合式函數
│   │   ├── useAuth.ts          # 認證相關
│   │   ├── useSchools.ts       # 學校相關
│   │   ├── useExperiences.ts   # 心得相關
│   │   ├── useForm.ts          # 表單相關
│   │   └── useNotification.ts  # 通知相關
│   │
│   └── plugins/                # Vue 插件
│       ├── element-plus.ts     # Element Plus 配置
│       ├── supabase.ts         # Supabase 配置
│       └── i18n.ts             # 國際化配置
│
├── tests/                      # 測試檔案
│   ├── unit/                   # 單元測試
│   │   ├── components/         # 組件測試
│   │   ├── stores/             # Store 測試
│   │   ├── utils/              # 工具函數測試
│   │   └── api/                # API 測試
│   │
│   ├── integration/            # 整合測試
│   │   ├── auth/               # 認證流程測試
│   │   ├── schools/            # 學校功能測試
│   │   └── experiences/        # 心得功能測試
│   │
│   └── e2e/                    # 端到端測試
│       ├── auth.spec.ts        # 認證測試
│       ├── schools.spec.ts     # 學校功能測試
│       └── experiences.spec.ts # 心得功能測試
│
├── docs/                       # 文件
│   ├── api/                    # API 文件
│   ├── components/             # 組件文件
│   └── deployment/             # 部署文件
│
└── scripts/                    # 腳本檔案
    ├── setup.sh                # 環境設置腳本
    ├── deploy.sh               # 部署腳本
    └── backup.sh               # 備份腳本
```

## 檔案命名規範

### 組件檔案
- 使用 PascalCase: `SchoolCard.vue`
- 頁面組件以 `Page` 結尾: `SchoolListPage.vue`
- 佈局組件以 `Layout` 結尾: `AppLayout.vue`

### 工具檔案
- 使用 camelCase: `apiClient.ts`
- 常數檔案使用 `constants.ts`
- 類型檔案使用對應名稱: `school.ts`

### 樣式檔案
- 使用 kebab-case: `main-styles.scss`
- 組件樣式與組件同名: `SchoolCard.scss`

## 模組化原則

### 組件設計
- 單一職責原則
- 可重用性
- 適當的 props 介面
- 清晰的 emit 事件

### 狀態管理
- 按功能模組分離
- 避免全域狀態污染
- 使用 TypeScript 類型定義
- 實作適當的持久化

### API 整合
- 按資源類型分離
- 統一的錯誤處理
- 類型安全的 API 調用
- 適當的快取策略

## 開發工作流程

### 功能開發
1. 創建功能分支
2. 實作組件和邏輯
3. 撰寫測試案例
4. 更新文件
5. 提交 Pull Request

### 程式碼審查
- 檢查程式碼品質
- 驗證功能完整性
- 確認測試覆蓋率
- 檢查文件更新

### 部署流程
- 自動化測試執行
- 程式碼品質檢查
- 建置和部署
- 監控和回滾 