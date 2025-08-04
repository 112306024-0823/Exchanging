# 政大商學院締約學校爬蟲使用指南

## 概述
本專案提供完整的政大商學院締約學校資料爬蟲解決方案，使用 Playwright MCP 和 Supabase MCP 工具。

## 檔案說明

### 1. `nccu_school_crawler.py`
完整的 Python 爬蟲程式，使用 Playwright 和 Supabase 直接整合。

### 2. `mcp_crawler.py`
MCP 版本的爬蟲框架，提供基本結構。

### 3. `run_crawler.py`
簡化的爬蟲執行腳本。

### 4. `actual_mcp_crawler.py`
實際使用 MCP 工具的爬蟲實作。

## 資料結構

### Schools 資料表結構
```sql
CREATE TABLE schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    city VARCHAR(100),
    exchange_quota INTEGER,
    degree_types TEXT[],
    description TEXT,
    official_website VARCHAR(500),
    location_info TEXT,
    image_url VARCHAR(500),
    nccu_page_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 爬蟲流程

### 第一階段：主頁面爬取
1. 訪問 https://outgoing-iep.nccu.edu.tw/school-list
2. 處理分頁（總共 11 頁）
3. 提取學校基本資訊：
   - 學校名稱
   - 國家
   - 城市
   - 交換名額
   - 學位類型
   - 學校圖片 URL
   - 詳細頁面連結

### 第二階段：詳細頁面爬取
1. 訪問每個學校的詳細頁面
2. 提取詳細資訊：
   - 學校介紹/描述
   - 學校官網連結
   - 地理位置資訊

### 第三階段：資料處理與儲存
1. 清理和標準化資料
2. 檢查重複資料
3. 儲存到 Supabase schools 表

## 使用 MCP 工具的實作方式

### Playwright MCP 使用
```python
# 導航到頁面
await mcp_playwright_browser_navigate(url="https://outgoing-iep.nccu.edu.tw/school-list")

# 獲取頁面快照
snapshot = await mcp_playwright_browser_snapshot()

# 解析頁面內容
schools = parse_schools_from_snapshot(snapshot)

# 訪問詳細頁面
for school in schools:
    await mcp_playwright_browser_navigate(url=school['nccu_page_url'])
    detail_snapshot = await mcp_playwright_browser_snapshot()
    detail_info = parse_school_detail_from_snapshot(detail_snapshot)
    school.update(detail_info)
```

### Supabase MCP 使用
```python
# 創建資料表
create_table_sql = """
CREATE TABLE IF NOT EXISTS schools (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    city VARCHAR(100),
    exchange_quota INTEGER,
    degree_types TEXT[],
    description TEXT,
    official_website VARCHAR(500),
    location_info TEXT,
    image_url VARCHAR(500),
    nccu_page_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
await mcp_supabase_execute_sql(sql=create_table_sql)

# 插入資料
for school in schools:
    cleaned_data = clean_school_data(school)
    await mcp_supabase_insert(table_name="schools", data=cleaned_data)
```

## 實際執行步驟

### 1. 環境準備
```bash
# 安裝依賴
pip install playwright httpx asyncio

# 安裝 Playwright 瀏覽器
playwright install
```

### 2. 配置 Supabase
- 確保您的 Supabase 專案 "Exchanging" 已創建
- 獲取 Supabase URL 和 API Key
- 在程式碼中更新配置

### 3. 執行爬蟲
```bash
# 執行完整爬蟲
python nccu_school_crawler.py

# 或執行 MCP 版本
python actual_mcp_crawler.py
```

## 資料解析規則

### 學校基本資訊提取
- **學校名稱**：從 `<h3>` 標籤中提取
- **國家**：從 "國家:" 後面的文字提取
- **城市**：從 "城市:" 後面的文字提取
- **交換名額**：從 "交換名額:" 後面的數字提取
- **學位類型**：從頁面中查找 Bachelor、Master、Ph.D 關鍵字
- **圖片 URL**：從 `<img>` 標籤的 `src` 屬性提取
- **詳細頁面連結**：從學校名稱連結的 `href` 屬性提取

### 學校詳細資訊提取
- **學校介紹**：從詳細頁面的段落文字中提取
- **學校官網**：從外部連結中提取
- **地理位置**：從包含位置相關關鍵字的文字中提取

## 錯誤處理

### 網路錯誤
- 實作重試機制
- 設定適當的等待時間
- 記錄錯誤詳情

### 資料解析錯誤
- 使用正則表達式進行容錯解析
- 提供預設值
- 記錄解析失敗的項目

### 資料庫錯誤
- 檢查資料完整性
- 處理重複資料
- 記錄插入失敗的項目

## 效能優化

### 並發處理
- 使用 asyncio 進行非同步處理
- 控制並發數量避免過度請求
- 實作請求間隔

### 資料快取
- 快取已處理的學校資料
- 避免重複訪問相同頁面
- 實作增量更新

### 記憶體管理
- 及時釋放不需要的資料
- 分批處理大量資料
- 監控記憶體使用情況

## 監控與日誌

### 日誌記錄
- 記錄爬取進度
- 記錄錯誤詳情
- 記錄效能指標

### 進度追蹤
- 顯示當前處理頁面
- 顯示已處理學校數量
- 顯示成功率統計

### 錯誤報告
- 生成錯誤摘要
- 提供重試建議
- 記錄失敗原因

## 注意事項

### 網站禮儀
- 遵守 robots.txt
- 設定適當的請求間隔
- 避免過度請求

### 資料品質
- 驗證資料完整性
- 清理異常資料
- 標準化資料格式

### 法律合規
- 確保爬蟲行為合法
- 遵守網站使用條款
- 保護個人隱私資料

## 故障排除

### 常見問題
1. **頁面載入失敗**：檢查網路連線和網站可用性
2. **資料解析錯誤**：檢查頁面結構是否變更
3. **資料庫連接失敗**：檢查 Supabase 配置和網路連線

### 解決方案
1. **重試機制**：自動重試失敗的請求
2. **備用方案**：提供多種解析策略
3. **錯誤恢復**：從失敗點繼續執行

## 未來改進

### 功能擴展
- 支援更多資料來源
- 實作資料更新機制
- 添加資料驗證功能

### 效能提升
- 實作分散式爬蟲
- 優化資料庫查詢
- 添加快取機制

### 監控增強
- 實作即時監控
- 添加告警機制
- 提供管理介面 