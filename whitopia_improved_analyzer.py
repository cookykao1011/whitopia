#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whitopia.jp 店鋪開業信息分析器 (改進版)
更好地分析和整理店鋪開業的詳細信息
"""

import json
import re
from datetime import datetime

class ImprovedWhitopiaAnalyzer:
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
            'prefecture': '',
            'date': '',
            'full_text': text
        }
        
        # 清理文字，移除多餘的空白和換行
        clean_text = re.sub(r'\s+', '', text)
        
        # 提取店鋪名稱 - 更精確的模式
        store_name_patterns = [
            r'「(ホワイトピア[^」]+店)」',
            r'(ホワイトピア[^が]+店)が',
            r'(ホワイトピア[^！]+店)！',
            r'(ホワイトピア\w+店)'
        ]
        
        for pattern in store_name_patterns:
            match = re.search(pattern, clean_text)
            if match:
                store_info['store_name'] = match.group(1)
                break
        
        # 提取都道府縣信息 - 更精確的模式
        prefecture_patterns = [
            r'新たに([^県]+県)に',
            r'([^県]+県)にOPEN',
            r'が新たに([^県]+県)',
            r'「[^」]+」が新たに([^県]+県)'
        ]
        
        for pattern in prefecture_patterns:
            match = re.search(pattern, clean_text)
            if match:
                store_info['prefecture'] = match.group(1)
                break
        
        # 提取日期
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})/(\d{1,2})/(\d{1,2})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) == 1:
                    store_info['date'] = match.group(1)
                else:
                    year, month, day = match.groups()
                    store_info['date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                break
        
        return store_info
    
    def analyze_store_openings(self):
        """分析店鋪開業信息"""
        data = self.load_data()
        if not data:
            return
        
        print("=" * 70)
        print("🏪 Whitopia.jp 店鋪開業信息詳細分析")
        print("=" * 70)
        print(f"📊 分析時間: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        print(f"📅 數據抓取時間: {data.get('scrape_time', '未知')}")
        print(f"📈 總共找到項目: {data.get('total_items', 0)} 個")
        print(f"🏬 店鋪相關項目: {data.get('store_related_items', 0)} 個")
        print()
        
        store_openings = []
        
        for item in data.get('store_news', []):
            full_text = item.get('content', '') + ' ' + item.get('title', '')
            store_info = self.extract_store_info(full_text)
            
            # 如果沒有從內容中提取到日期，使用項目的日期
            if not store_info['date'] and item.get('date'):
                store_info['date'] = item['date']
            
            store_info['match_keyword'] = item.get('match_keyword', '')
            store_info['url'] = item.get('url', '')
            
            store_openings.append(store_info)
        
        # 按日期排序（最新的在前）
        store_openings.sort(key=lambda x: x['date'] if x['date'] else '0000-00-00', reverse=True)
        
        print("🗓️ 店鋪開業時間表:")
        print("=" * 70)
        
        for i, store in enumerate(store_openings, 1):
            if store['date']:
                try:
                    date_obj = datetime.strptime(store['date'], '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%Y年%m月%d日')
                    weekday = ['月', '火', '水', '木', '金', '土', '日'][date_obj.weekday()]
                    date_display = f"{formatted_date} ({weekday})"
                except:
                    date_display = store['date']
            else:
                date_display = "日期未知"
            
            print(f"🏪 {i}. {store['store_name'] or '店名未知'}")
            print(f"   📅 開業日期: {date_display}")
            print(f"   📍 所在地區: {store['prefecture'] or '地區未知'}")
            print(f"   🔍 關鍵詞: {store['match_keyword']}")
            print(f"   🔗 URL: {store['url']}")
            
            # 顯示原始文字的關鍵部分
            key_text = store['full_text'][:150].replace('\n', ' ')
            print(f"   📝 內容摘要: {key_text}...")
            print("-" * 70)
        
        # 統計分析
        print("\n📊 統計分析:")
        print("=" * 70)
        
        # 按月份統計
        monthly_stats = {}
        prefecture_stats = {}
        
        for store in store_openings:
            if store['date']:
                try:
                    month = store['date'][:7]  # YYYY-MM
                    monthly_stats[month] = monthly_stats.get(month, 0) + 1
                except:
                    pass
            
            if store['prefecture']:
                prefecture_stats[store['prefecture']] = prefecture_stats.get(store['prefecture'], 0) + 1
        
        print("📅 按月份統計:")
        for month, count in sorted(monthly_stats.items(), reverse=True):
            try:
                month_obj = datetime.strptime(month + '-01', '%Y-%m-%d')
                month_display = month_obj.strftime('%Y年%m月')
                print(f"   {month_display}: {count} 家店鋪")
            except:
                print(f"   {month}: {count} 家店鋪")
        
        print("\n📍 按地區統計:")
        for prefecture, count in sorted(prefecture_stats.items(), key=lambda x: x[1], reverse=True):
            print(f"   {prefecture}: {count} 家店鋪")
        
        # 生成摘要報告
        print(f"\n📋 摘要報告:")
        print("=" * 70)
        total_stores = len([s for s in store_openings if s['store_name']])
        print(f"✅ 成功識別店鋪數量: {total_stores} 家")
        print(f"📍 涉及地區數量: {len(prefecture_stats)} 個都道府縣")
        print(f"📅 開業時間跨度: {min(monthly_stats.keys()) if monthly_stats else '未知'} 至 {max(monthly_stats.keys()) if monthly_stats else '未知'}")
        
        # 保存詳細分析結果
        analysis_result = {
            'analysis_time': datetime.now().isoformat(),
            'total_stores': total_stores,
            'store_openings': store_openings,
            'monthly_stats': monthly_stats,
            'prefecture_stats': prefecture_stats,
            'summary': {
                'total_identified_stores': total_stores,
                'prefectures_count': len(prefecture_stats),
                'date_range': {
                    'start': min(monthly_stats.keys()) if monthly_stats else None,
                    'end': max(monthly_stats.keys()) if monthly_stats else None
                }
            }
        }
        
        with open('whitopia_detailed_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 詳細分析結果已保存到 whitopia_detailed_analysis.json")
        
        return analysis_result

if __name__ == "__main__":
    analyzer = ImprovedWhitopiaAnalyzer()
    analyzer.analyze_store_openings()