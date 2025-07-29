#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whitopia.jp 店鋪開業信息分析器
分析爬蟲結果並整理店鋪開業的詳細信息
"""

import json
import re
from datetime import datetime

class WhitopiaAnalyzer:
    def __init__(self, json_file='whitopia_news.json'):
        self.json_file = json_file
        self.store_openings = []
    
    def load_data(self):
        """載入JSON數據"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"找不到文件: {self.json_file}")
            return None
        except json.JSONDecodeError:
            print(f"JSON格式錯誤: {self.json_file}")
            return None
    
    def extract_store_info(self, text):
        """從文字中提取店鋪信息"""
        store_info = {
            'store_name': '',
            'location': '',
            'date': '',
            'prefecture': ''
        }
        
        # 提取店鋪名稱
        store_name_patterns = [
            r'「(ホワイトピア[^」]+)」',
            r'(ホワイトピア[^\s]+店)',
            r'(ホワイトピア[^が]+)が'
        ]
        
        for pattern in store_name_patterns:
            match = re.search(pattern, text)
            if match:
                store_info['store_name'] = match.group(1)
                break
        
        # 提取地點信息
        location_patterns = [
            r'([^県]+県)に',
            r'新たに([^県]+県)',
            r'([^県]+県)にOPEN'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                store_info['prefecture'] = match.group(1)
                break
        
        # 提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if date_match:
            store_info['date'] = date_match.group(1)
        
        return store_info
    
    def analyze_store_openings(self):
        """分析店鋪開業信息"""
        data = self.load_data()
        if not data:
            return
        
        print("=" * 60)
        print("Whitopia.jp 店鋪開業信息分析結果")
        print("=" * 60)
        print(f"分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"數據來源: {data.get('scrape_time', '未知')}")
        print(f"總共找到 {data.get('total_items', 0)} 個項目")
        print(f"店鋪相關項目: {data.get('store_related_items', 0)} 個")
        print()
        
        store_openings = []
        
        for item in data.get('store_news', []):
            store_info = self.extract_store_info(item.get('content', '') + ' ' + item.get('title', ''))
            
            # 如果沒有從內容中提取到日期，使用項目的日期
            if not store_info['date'] and item.get('date'):
                store_info['date'] = item['date']
            
            store_info['raw_content'] = item.get('content', '')
            store_info['match_keyword'] = item.get('match_keyword', '')
            
            store_openings.append(store_info)
        
        # 按日期排序（最新的在前）
        store_openings.sort(key=lambda x: x['date'], reverse=True)
        
        print("📅 店鋪開業時間表:")
        print("-" * 60)
        
        for i, store in enumerate(store_openings, 1):
            date_obj = datetime.strptime(store['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%Y年%m月%d日')
            
            print(f"{i}. 開業日期: {formatted_date}")
            print(f"   店鋪名稱: {store['store_name']}")
            print(f"   所在地區: {store['prefecture']}")
            print(f"   關鍵詞: {store['match_keyword']}")
            print(f"   原始內容: {store['raw_content'][:100]}...")
            print()
        
        # 統計分析
        print("📊 統計分析:")
        print("-" * 60)
        
        # 按月份統計
        monthly_stats = {}
        prefecture_stats = {}
        
        for store in store_openings:
            if store['date']:
                month = store['date'][:7]  # YYYY-MM
                monthly_stats[month] = monthly_stats.get(month, 0) + 1
            
            if store['prefecture']:
                prefecture_stats[store['prefecture']] = prefecture_stats.get(store['prefecture'], 0) + 1
        
        print("按月份統計:")
        for month, count in sorted(monthly_stats.items(), reverse=True):
            print(f"  {month}: {count} 家店鋪")
        
        print("\n按地區統計:")
        for prefecture, count in sorted(prefecture_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {prefecture}: {count} 家店鋪")
        
        # 保存分析結果
        analysis_result = {
            'analysis_time': datetime.now().isoformat(),
            'total_stores': len(store_openings),
            'store_openings': store_openings,
            'monthly_stats': monthly_stats,
            'prefecture_stats': prefecture_stats
        }
        
        with open('whitopia_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"\n詳細分析結果已保存到 whitopia_analysis.json")
        
        return analysis_result

if __name__ == "__main__":
    analyzer = WhitopiaAnalyzer()
    analyzer.analyze_store_openings()