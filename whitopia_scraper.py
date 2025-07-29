#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whitopia.jp お知らせ爬蟲
用於抓取網站的公告信息，特別是店鋪開業相關的信息
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
import urllib.parse

class WhitopiaScraper:
    def __init__(self):
        self.base_url = "https://www.whitopia.jp"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page(self, url, retries=3):
        """獲取網頁內容"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response
            except requests.RequestException as e:
                print(f"嘗試 {attempt + 1} 失敗: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    raise
    
    def scrape_news_list(self):
        """抓取お知らせ列表"""
        print("正在抓取主頁面...")
        
        try:
            response = self.get_page(self.base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尋找お知らせ相關的元素
            news_items = []
            
            # 常見的新聞/公告選擇器
            selectors = [
                '.news-item', '.news-list li', '.information-item',
                '.notice-item', '.announcement-item', 'article',
                '.post', '.entry', '.item'
            ]
            
            # 嘗試不同的選擇器
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    print(f"找到 {len(items)} 個項目使用選擇器: {selector}")
                    for item in items:
                        news_items.append(self.parse_news_item(item))
                    break
            
            # 如果沒有找到特定結構，嘗試尋找包含日期和文字的元素
            if not news_items:
                print("嘗試尋找包含日期的文字...")
                date_pattern = r'(\d{4})[年/.-](\d{1,2})[月/.-](\d{1,2})'
                all_text = soup.get_text()
                
                # 尋找所有包含日期的行
                lines = all_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if re.search(date_pattern, line) and len(line) > 10:
                        news_items.append({
                            'date': self.extract_date(line),
                            'title': line,
                            'content': line,
                            'url': self.base_url
                        })
            
            return news_items
            
        except Exception as e:
            print(f"抓取失敗: {e}")
            return []
    
    def parse_news_item(self, item):
        """解析單個新聞項目"""
        try:
            # 提取日期
            date_text = ""
            date_elements = item.find_all(text=re.compile(r'\d{4}[年/.-]\d{1,2}[月/.-]\d{1,2}'))
            if date_elements:
                date_text = date_elements[0].strip()
            
            # 提取標題
            title = ""
            title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'])
            if title_elem:
                title = title_elem.get_text().strip()
            else:
                title = item.get_text().strip()[:100]
            
            # 提取鏈接
            link = ""
            link_elem = item.find('a')
            if link_elem and link_elem.get('href'):
                link = urllib.parse.urljoin(self.base_url, link_elem['href'])
            
            return {
                'date': self.extract_date(date_text + " " + title),
                'title': title,
                'content': item.get_text().strip(),
                'url': link or self.base_url
            }
            
        except Exception as e:
            print(f"解析項目失敗: {e}")
            return None
    
    def extract_date(self, text):
        """從文字中提取日期"""
        date_patterns = [
            r'(\d{4})[年](\d{1,2})[月](\d{1,2})[日]',
            r'(\d{4})[/](\d{1,2})[/](\d{1,2})',
            r'(\d{4})[-](\d{1,2})[-](\d{1,2})',
            r'(\d{4})[.](\d{1,2})[.](\d{1,2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                try:
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    continue
        
        return ""
    
    def filter_store_opening_news(self, news_items):
        """過濾出店鋪開業相關的新聞"""
        store_keywords = [
            '開店', '開業', 'オープン', 'OPEN', 'open', '新店',
            '店舗', '出店', '開設', 'グランドオープン', 'プレオープン',
            '新規', '新しい', '開始', 'スタート'
        ]
        
        store_news = []
        for item in news_items:
            if not item:
                continue
                
            text = (item.get('title', '') + ' ' + item.get('content', '')).lower()
            
            for keyword in store_keywords:
                if keyword.lower() in text:
                    item['match_keyword'] = keyword
                    store_news.append(item)
                    break
        
        return store_news
    
    def scrape_detailed_page(self, url):
        """抓取詳細頁面內容"""
        try:
            response = self.get_page(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除腳本和樣式
            for script in soup(["script", "style"]):
                script.decompose()
            
            content = soup.get_text()
            return content.strip()
            
        except Exception as e:
            print(f"抓取詳細頁面失敗 {url}: {e}")
            return ""
    
    def run_scraper(self):
        """執行爬蟲"""
        print("=" * 50)
        print("Whitopia.jp お知らせ 爬蟲開始")
        print("=" * 50)
        
        # 抓取新聞列表
        news_items = self.scrape_news_list()
        print(f"\n總共找到 {len(news_items)} 個項目")
        
        # 過濾店鋪開業相關新聞
        store_news = self.filter_store_opening_news(news_items)
        print(f"找到 {len(store_news)} 個可能與店鋪開業相關的項目")
        
        # 保存結果
        results = {
            'scrape_time': datetime.now().isoformat(),
            'total_items': len(news_items),
            'store_related_items': len(store_news),
            'all_news': news_items,
            'store_news': store_news
        }
        
        # 輸出結果
        print("\n" + "=" * 50)
        print("店鋪開業相關信息:")
        print("=" * 50)
        
        if store_news:
            for i, item in enumerate(store_news, 1):
                print(f"\n{i}. 日期: {item.get('date', '未知')}")
                print(f"   標題: {item.get('title', '無標題')}")
                print(f"   關鍵詞: {item.get('match_keyword', '無')}")
                print(f"   URL: {item.get('url', '無')}")
                print(f"   內容預覽: {item.get('content', '')[:200]}...")
        else:
            print("未找到明確的店鋪開業信息")
        
        print("\n" + "=" * 50)
        print("所有新聞項目:")
        print("=" * 50)
        
        for i, item in enumerate(news_items[:10], 1):  # 只顯示前10個
            if item:
                print(f"\n{i}. 日期: {item.get('date', '未知')}")
                print(f"   標題: {item.get('title', '無標題')[:100]}")
                print(f"   內容: {item.get('content', '')[:150]}...")
        
        # 保存到JSON文件
        with open('whitopia_news.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n結果已保存到 whitopia_news.json")
        return results

if __name__ == "__main__":
    scraper = WhitopiaScraper()
    scraper.run_scraper()