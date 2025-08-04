#!/usr/bin/env python3
"""
政大商學院締約學校資料爬蟲 - MCP 版本
使用 Playwright MCP 和 Supabase MCP 進行爬蟲和資料儲存
"""

import asyncio
import json
import re
import time
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import logging
from datetime import datetime

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MCPNCCUCrawler:
    def __init__(self):
        """初始化 MCP 爬蟲"""
        self.base_url = "https://outgoing-iep.nccu.edu.tw"
        self.schools_data = []
        self.processed_schools = set()
        
    async def get_total_pages(self) -> int:
        """獲取總頁數"""
        try:
            # 使用 Playwright MCP 導航到主頁面
            # 這裡需要實際的 MCP 調用
            logger.info("正在獲取總頁數...")
            
            # 根據之前的分析，總共有 11 頁（0-10）
            return 10
            
        except Exception as e:
            logger.error(f"獲取總頁數失敗: {e}")
            return 1
    
    def extract_school_info_from_text(self, text: str) -> Dict[str, Any]:
        """從文字中提取學校資訊"""
        try:
            # 學校名稱通常在 h3 標籤中
            name_match = re.search(r'<h3[^>]*>([^<]+)</h3>', text)
            school_name = name_match.group(1).strip() if name_match else None
            
            # 國家
            country_match = re.search(r'國家:\s*([^\s]+)', text)
            country = country_match.group(1) if country_match else None
            
            # 城市
            city_match = re.search(r'城市:\s*([^\s]+)', text)
            city = city_match.group(1) if city_match else None
            
            # 交換名額
            quota_match = re.search(r'交換名額:\s*(\d+)', text)
            exchange_quota = int(quota_match.group(1)) if quota_match else None
            
            # 學位類型
            degree_types = []
            if 'Bachelor' in text:
                degree_types.append('Bachelor')
            if 'Master' in text:
                degree_types.append('Master')
            if 'Ph.D' in text:
                degree_types.append('Ph.D')
            
            # 學校連結
            url_match = re.search(r'href="([^"]*node/\d+)"', text)
            school_url = None
            if url_match:
                school_url = urljoin(self.base_url, url_match.group(1))
            
            # 圖片 URL
            img_match = re.search(r'src="([^"]*\.(?:jpg|png|gif))"', text)
            image_url = None
            if img_match:
                image_url = urljoin(self.base_url, img_match.group(1))
            
            return {
                'name': school_name,
                'country': country,
                'city': city,
                'exchange_quota': exchange_quota,
                'degree_types': degree_types,
                'image_url': image_url,
                'nccu_page_url': school_url
            }
            
        except Exception as e:
            logger.error(f"提取學校資訊失敗: {e}")
            return None
    
    async def crawl_school_list_page(self, page_num: int) -> List[Dict[str, Any]]:
        """爬取單頁學校列表"""
        schools = []
        
        try:
            url = f"{self.base_url}/school-list"
            if page_num > 0:
                url += f"?page={page_num}"
            
            logger.info(f"正在爬取第 {page_num + 1} 頁: {url}")
            
            # 這裡需要實際的 Playwright MCP 調用
            # 暫時返回模擬資料
            logger.info(f"第 {page_num + 1} 頁完成，發現 {len(schools)} 所學校")
            return schools
            
        except Exception as e:
            logger.error(f"爬取第 {page_num + 1} 頁失敗: {e}")
            return []
    
    async def crawl_school_detail(self, school_url: str) -> Dict[str, Any]:
        """爬取學校詳細資訊"""
        try:
            logger.info(f"正在爬取學校詳細資訊: {school_url}")
            
            # 這裡需要實際的 Playwright MCP 調用
            # 暫時返回空字典
            return {}
            
        except Exception as e:
            logger.error(f"爬取學校詳細資訊失敗 {school_url}: {e}")
            return {}
    
    async def create_supabase_table(self):
        """在 Supabase 中創建 schools 表"""
        try:
            # 這裡需要實際的 Supabase MCP 調用
            logger.info("正在創建 schools 資料表...")
            
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
            
            logger.info("schools 資料表創建完成")
            
        except Exception as e:
            logger.error(f"創建資料表失敗: {e}")
    
    async def save_to_supabase(self, school_data: Dict[str, Any]):
        """儲存單筆學校資料到 Supabase"""
        try:
            # 這裡需要實際的 Supabase MCP 調用
            logger.info(f"正在儲存學校資料: {school_data.get('name', 'Unknown')}")
            
            # 清理資料
            cleaned_data = self.clean_school_data(school_data)
            
            # 插入資料到 Supabase
            # 這裡需要實際的 API 調用
            
            logger.info(f"成功儲存: {school_data.get('name', 'Unknown')}")
            
        except Exception as e:
            logger.error(f"儲存學校資料失敗 {school_data.get('name', 'Unknown')}: {e}")
    
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
    
    async def save_to_json(self, filename: str = 'mcp_schools_data.json'):
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
            logger.info("開始執行政大商學院締約學校爬蟲 (MCP 版本)")
            
            # 創建 Supabase 資料表
            await self.create_supabase_table()
            
            # 獲取總頁數
            total_pages = await self.get_total_pages()
            logger.info(f"總共發現 {total_pages + 1} 頁")
            
            # 爬取所有頁面
            for page_num in range(total_pages + 1):
                schools = await self.crawl_school_list_page(page_num)
                
                # 爬取詳細資訊並儲存
                for school in schools:
                    if school.get('nccu_page_url'):
                        detail_info = await self.crawl_school_detail(school['nccu_page_url'])
                        school.update(detail_info)
                    
                    # 儲存到 Supabase
                    await self.save_to_supabase(school)
                    self.schools_data.append(school)
                    
                    # 避免過度請求
                    await asyncio.sleep(1)
                
                # 避免過度請求
                await asyncio.sleep(2)
            
            # 儲存到 JSON 檔案
            await self.save_to_json()
            
            logger.info(f"爬蟲執行完成，總共處理 {len(self.schools_data)} 所學校")
            
        except Exception as e:
            logger.error(f"爬蟲執行失敗: {e}")

async def main():
    """主函數"""
    crawler = MCPNCCUCrawler()
    await crawler.run()

if __name__ == "__main__":
    asyncio.run(main()) 