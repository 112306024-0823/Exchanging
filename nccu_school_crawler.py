#!/usr/bin/env python3
"""
政大商學院締約學校資料爬蟲
使用 Playwright 爬取學校資料並儲存到 Supabase
"""

import asyncio
import json
import re
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NCCUSchoolCrawler:
    def __init__(self, supabase_url: str, supabase_key: str):
        """
        初始化爬蟲
        
        Args:
            supabase_url: Supabase 專案 URL
            supabase_key: Supabase API Key
        """
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.base_url = "https://outgoing-iep.nccu.edu.tw"
        self.schools_data = []
        self.processed_schools = set()
        
    async def init_browser(self):
        """初始化 Playwright 瀏覽器"""
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.page = await self.browser.new_page()
            
            # 設置用戶代理
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            logger.info("瀏覽器初始化完成")
            
        except Exception as e:
            logger.error(f"瀏覽器初始化失敗: {e}")
            raise
    
    async def close_browser(self):
        """關閉瀏覽器"""
        if hasattr(self, 'browser'):
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
        logger.info("瀏覽器已關閉")
    
    async def get_total_pages(self) -> int:
        """獲取總頁數"""
        try:
            await self.page.goto(f"{self.base_url}/school-list")
            await self.page.wait_for_load_state('networkidle')
            
            # 檢查分頁資訊
            pagination = await self.page.query_selector('.pager')
            if pagination:
                # 尋找最後一頁的連結
                last_page_link = await pagination.query_selector('a[href*="last"]')
                if last_page_link:
                    href = await last_page_link.get_attribute('href')
                    if href and 'page=' in href:
                        match = re.search(r'page=(\d+)', href)
                        if match:
                            return int(match.group(1))
                
                # 如果沒有 last 連結，計算所有頁面連結
                page_links = await pagination.query_selector_all('a[href*="page="]')
                max_page = 0
                for link in page_links:
                    href = await link.get_attribute('href')
                    if href:
                        match = re.search(r'page=(\d+)', href)
                        if match:
                            page_num = int(match.group(1))
                            max_page = max(max_page, page_num)
                
                return max_page if max_page > 0 else 1
            
            return 1
            
        except Exception as e:
            logger.error(f"獲取總頁數失敗: {e}")
            return 1
    
    async def extract_school_basic_info(self, school_element) -> Dict[str, Any]:
        """從學校元素中提取基本資訊"""
        try:
            # 學校名稱和連結
            name_link = await school_element.query_selector('h3 a')
            if not name_link:
                return None
            
            school_name = await name_link.text_content()
            school_url = await name_link.get_attribute('href')
            if school_url:
                school_url = urljoin(self.base_url, school_url)
            
            # 學校圖片
            img_element = await school_element.query_selector('img')
            image_url = None
            if img_element:
                image_url = await img_element.get_attribute('src')
                if image_url:
                    image_url = urljoin(self.base_url, image_url)
            
            # 提取詳細資訊
            info_text = await school_element.text_content()
            
            # 國家
            country_match = re.search(r'國家:\s*([^\s]+)', info_text)
            country = country_match.group(1) if country_match else None
            
            # 城市
            city_match = re.search(r'城市:\s*([^\s]+)', info_text)
            city = city_match.group(1) if city_match else None
            
            # 交換名額
            quota_match = re.search(r'交換名額:\s*(\d+)', info_text)
            exchange_quota = int(quota_match.group(1)) if quota_match else None
            
            # 學位類型
            degree_types = []
            if 'Bachelor' in info_text:
                degree_types.append('Bachelor')
            if 'Master' in info_text:
                degree_types.append('Master')
            if 'Ph.D' in info_text:
                degree_types.append('Ph.D')
            
            return {
                'name': school_name.strip() if school_name else None,
                'country': country,
                'city': city,
                'exchange_quota': exchange_quota,
                'degree_types': degree_types,
                'image_url': image_url,
                'nccu_page_url': school_url
            }
            
        except Exception as e:
            logger.error(f"提取學校基本資訊失敗: {e}")
            return None
    
    async def crawl_school_list_page(self, page_num: int) -> List[Dict[str, Any]]:
        """爬取單頁學校列表"""
        schools = []
        
        try:
            url = f"{self.base_url}/school-list"
            if page_num > 0:
                url += f"?page={page_num}"
            
            logger.info(f"正在爬取第 {page_num + 1} 頁: {url}")
            await self.page.goto(url)
            await self.page.wait_for_load_state('networkidle')
            
            # 等待表格載入
            await self.page.wait_for_selector('table', timeout=10000)
            
            # 找到所有學校元素
            school_elements = await self.page.query_selector_all('table tr td')
            
            for element in school_elements:
                # 檢查是否包含學校資訊
                school_info = await self.extract_school_basic_info(element)
                if school_info and school_info['name']:
                    # 檢查是否已處理過
                    if school_info['nccu_page_url'] not in self.processed_schools:
                        schools.append(school_info)
                        self.processed_schools.add(school_info['nccu_page_url'])
                        logger.info(f"發現學校: {school_info['name']}")
            
            logger.info(f"第 {page_num + 1} 頁完成，發現 {len(schools)} 所學校")
            return schools
            
        except Exception as e:
            logger.error(f"爬取第 {page_num + 1} 頁失敗: {e}")
            return []
    
    async def extract_school_detail_info(self, school_url: str) -> Dict[str, Any]:
        """爬取學校詳細資訊"""
        try:
            logger.info(f"正在爬取學校詳細資訊: {school_url}")
            await self.page.goto(school_url)
            await self.page.wait_for_load_state('networkidle')
            
            detail_info = {}
            
            # 學校介紹
            intro_element = await self.page.query_selector('p')
            if intro_element:
                description = await intro_element.text_content()
                detail_info['description'] = description.strip() if description else None
            
            # 學校官網
            website_element = await self.page.query_selector('a[href*="http"]')
            if website_element:
                website_url = await website_element.get_attribute('href')
                if website_url and not website_url.startswith(self.base_url):
                    detail_info['official_website'] = website_url
            
            # 地理位置資訊
            location_elements = await self.page.query_selector_all('div')
            location_info = []
            for element in location_elements:
                text = await element.text_content()
                if text and any(keyword in text for keyword in ['Location', 'Address', '地址', '位置']):
                    location_info.append(text.strip())
            
            if location_info:
                detail_info['location_info'] = ' '.join(location_info)
            
            logger.info(f"學校詳細資訊爬取完成: {school_url}")
            return detail_info
            
        except Exception as e:
            logger.error(f"爬取學校詳細資訊失敗 {school_url}: {e}")
            return {}
    
    async def crawl_all_schools(self):
        """爬取所有學校資料"""
        try:
            total_pages = await self.get_total_pages()
            logger.info(f"總共發現 {total_pages + 1} 頁")
            
            all_schools = []
            
            # 爬取所有頁面
            for page_num in range(total_pages + 1):
                schools = await self.crawl_school_list_page(page_num)
                all_schools.extend(schools)
                
                # 避免過度請求
                await asyncio.sleep(2)
            
            logger.info(f"總共發現 {len(all_schools)} 所學校")
            
            # 爬取詳細資訊
            for i, school in enumerate(all_schools):
                if school.get('nccu_page_url'):
                    detail_info = await self.extract_school_detail_info(school['nccu_page_url'])
                    school.update(detail_info)
                    
                    logger.info(f"進度: {i + 1}/{len(all_schools)} - {school['name']}")
                    
                    # 避免過度請求
                    await asyncio.sleep(1)
            
            self.schools_data = all_schools
            logger.info("所有學校資料爬取完成")
            
        except Exception as e:
            logger.error(f"爬取所有學校資料失敗: {e}")
    
    async def save_to_supabase(self):
        """儲存資料到 Supabase"""
        try:
            import httpx
            
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            }
            
            # 首先創建 schools 表（如果不存在）
            await self.create_schools_table()
            
            # 儲存學校資料
            success_count = 0
            error_count = 0
            
            for school in self.schools_data:
                try:
                    # 清理資料
                    cleaned_school = self.clean_school_data(school)
                    
                    # 插入資料
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            f"{self.supabase_url}/rest/v1/schools",
                            headers=headers,
                            json=cleaned_school
                        )
                        
                        if response.status_code == 201:
                            success_count += 1
                            logger.info(f"成功儲存: {school['name']}")
                        else:
                            error_count += 1
                            logger.error(f"儲存失敗 {school['name']}: {response.text}")
                    
                    # 避免過度請求
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"儲存學校資料失敗 {school.get('name', 'Unknown')}: {e}")
            
            logger.info(f"資料儲存完成: 成功 {success_count} 筆，失敗 {error_count} 筆")
            
        except Exception as e:
            logger.error(f"儲存到 Supabase 失敗: {e}")
    
    async def create_schools_table(self):
        """創建 schools 資料表"""
        try:
            import httpx
            
            headers = {
                'apikey': self.supabase_key,
                'Authorization': f'Bearer {self.supabase_key}',
                'Content-Type': 'application/json'
            }
            
            # SQL 創建表語句
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
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supabase_url}/rest/v1/rpc/exec_sql",
                    headers=headers,
                    json={'sql': create_table_sql}
                )
                
                if response.status_code == 200:
                    logger.info("schools 資料表創建成功")
                else:
                    logger.warning(f"創建資料表可能失敗: {response.text}")
            
        except Exception as e:
            logger.error(f"創建資料表失敗: {e}")
    
    def clean_school_data(self, school: Dict[str, Any]) -> Dict[str, Any]:
        """清理學校資料"""
        cleaned = {}
        
        # 基本資訊
        cleaned['name'] = school.get('name', '').strip()
        cleaned['country'] = school.get('country', '').strip()
        cleaned['city'] = school.get('city', '').strip()
        cleaned['exchange_quota'] = school.get('exchange_quota')
        cleaned['degree_types'] = school.get('degree_types', [])
        
        # 詳細資訊
        cleaned['description'] = school.get('description', '').strip()
        cleaned['official_website'] = school.get('official_website', '').strip()
        cleaned['location_info'] = school.get('location_info', '').strip()
        cleaned['image_url'] = school.get('image_url', '').strip()
        cleaned['nccu_page_url'] = school.get('nccu_page_url', '').strip()
        
        # 移除空值
        cleaned = {k: v for k, v in cleaned.items() if v is not None and v != ''}
        
        return cleaned
    
    async def save_to_json(self, filename: str = 'schools_data.json'):
        """儲存資料到 JSON 檔案"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.schools_data, f, ensure_ascii=False, indent=2)
            logger.info(f"資料已儲存到 {filename}")
        except Exception as e:
            logger.error(f"儲存 JSON 檔案失敗: {e}")
    
    async def run(self):
        """執行完整的爬蟲流程"""
        try:
            logger.info("開始執行政大商學院締約學校爬蟲")
            
            # 初始化瀏覽器
            await self.init_browser()
            
            # 爬取所有學校資料
            await self.crawl_all_schools()
            
            # 儲存到 JSON 檔案
            await self.save_to_json()
            
            # 儲存到 Supabase
            await self.save_to_supabase()
            
            logger.info("爬蟲執行完成")
            
        except Exception as e:
            logger.error(f"爬蟲執行失敗: {e}")
        finally:
            await self.close_browser()

async def main():
    """主函數"""
    # Supabase 配置
    SUPABASE_URL = "https://bhecrttazqsflquqzzwn.supabase.co"  # 您的 Exchanging 專案 URL
    SUPABASE_KEY = "your_supabase_anon_key"  # 請替換為您的 Supabase anon key
    
    # 創建爬蟲實例
    crawler = NCCUSchoolCrawler(SUPABASE_URL, SUPABASE_KEY)
    
    # 執行爬蟲
    await crawler.run()

if __name__ == "__main__":
    asyncio.run(main()) 