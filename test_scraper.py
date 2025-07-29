#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Whitopia.jp 爬蟲測試腳本
用於驗證爬蟲功能是否正常運行
"""

import sys
import traceback

def test_imports():
    """測試必要的庫導入"""
    print("🔍 測試庫導入...")
    try:
        import requests
        import bs4
        import json
        import re
        from datetime import datetime
        print("✅ 所有必要的庫導入成功")
        return True
    except ImportError as e:
        print(f"❌ 庫導入失敗: {e}")
        return False

def test_network_connection():
    """測試網絡連接"""
    print("\n🌐 測試網絡連接...")
    try:
        import requests
        response = requests.get('https://www.whitopia.jp', timeout=15)
        if response.status_code == 200:
            print(f"✅ 網站連接成功，狀態碼: {response.status_code}")
            print(f"   響應大小: {len(response.text)} 字符")
            return True
        else:
            print(f"⚠️ 網站響應異常，狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 網絡連接失敗: {e}")
        return False

def test_scraper_basic():
    """測試爬蟲基本功能"""
    print("\n🕷️ 測試爬蟲基本功能...")
    try:
        from whitopia_scraper import WhitopiaScraper
        scraper = WhitopiaScraper()
        
        # 測試獲取頁面
        response = scraper.get_page(scraper.base_url)
        if response:
            print("✅ 頁面獲取成功")
            
            # 測試解析功能
            news_items = scraper.scrape_news_list()
            if news_items:
                print(f"✅ 成功解析 {len(news_items)} 個新聞項目")
                
                # 測試過濾功能
                store_news = scraper.filter_store_opening_news(news_items)
                print(f"✅ 找到 {len(store_news)} 個店鋪相關項目")
                
                return True
            else:
                print("⚠️ 未找到新聞項目")
                return False
        else:
            print("❌ 頁面獲取失敗")
            return False
            
    except Exception as e:
        print(f"❌ 爬蟲測試失敗: {e}")
        traceback.print_exc()
        return False

def test_analyzer():
    """測試分析器功能"""
    print("\n📊 測試分析器功能...")
    try:
        import os
        if os.path.exists('whitopia_news.json'):
            from whitopia_improved_analyzer import ImprovedWhitopiaAnalyzer
            analyzer = ImprovedWhitopiaAnalyzer()
            data = analyzer.load_data()
            
            if data:
                print("✅ JSON數據載入成功")
                print(f"   總項目數: {data.get('total_items', 0)}")
                print(f"   店鋪相關項目: {data.get('store_related_items', 0)}")
                return True
            else:
                print("❌ JSON數據載入失敗")
                return False
        else:
            print("⚠️ 找不到 whitopia_news.json 文件，請先運行爬蟲")
            return False
            
    except Exception as e:
        print(f"❌ 分析器測試失敗: {e}")
        return False

def run_full_test():
    """運行完整測試"""
    print("🚀 開始 Whitopia.jp 爬蟲完整測試")
    print("=" * 50)
    
    tests = [
        ("庫導入測試", test_imports),
        ("網絡連接測試", test_network_connection),
        ("爬蟲功能測試", test_scraper_basic),
        ("分析器測試", test_analyzer)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 執行出錯: {e}")
            results.append((test_name, False))
    
    # 總結測試結果
    print("\n" + "=" * 50)
    print("📋 測試結果總結:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{len(results)} 個測試通過")
    
    if passed == len(results):
        print("\n🎉 所有測試通過！爬蟲已準備就緒")
        print("\n📝 使用方法:")
        print("   python3 whitopia_scraper.py          # 運行爬蟲")
        print("   python3 whitopia_improved_analyzer.py # 運行分析器")
    else:
        print(f"\n⚠️ 有 {len(results) - passed} 個測試失敗，請檢查上述錯誤信息")
    
    return passed == len(results)

if __name__ == "__main__":
    success = run_full_test()
    sys.exit(0 if success else 1)