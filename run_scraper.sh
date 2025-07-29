#!/bin/bash
# Whitopia.jp 爬蟲運行腳本

echo "🚀 開始運行 Whitopia.jp 店鋪開業信息爬蟲"
echo "================================================"

# 檢查當前目錄
echo "📁 當前工作目錄: $(pwd)"
echo ""

# 第一步：運行爬蟲
echo "🕷️ 第一步：運行爬蟲抓取數據..."
python3 whitopia_scraper.py

if [ $? -eq 0 ]; then
    echo "✅ 爬蟲運行成功！"
    echo ""
    
    # 第二步：分析數據
    echo "📊 第二步：分析抓取的數據..."
    python3 whitopia_improved_analyzer.py
    
    if [ $? -eq 0 ]; then
        echo "✅ 數據分析完成！"
        echo ""
        
        # 顯示結果文件
        echo "📋 生成的結果文件："
        echo "================================================"
        ls -la *.json *.md | grep -E "(whitopia_|README)" | while read line; do
            echo "   $line"
        done
        
        echo ""
        echo "🎉 爬蟲運行完成！結果已保存到以上文件中。"
        echo ""
        echo "📖 如何查看結果："
        echo "   - 查看詳細報告: cat whitopia_report.md"
        echo "   - 查看JSON數據: cat whitopia_detailed_analysis.json"
        echo "   - 查看原始數據: cat whitopia_news.json"
        
    else
        echo "❌ 數據分析失敗"
        exit 1
    fi
else
    echo "❌ 爬蟲運行失敗"
    exit 1
fi