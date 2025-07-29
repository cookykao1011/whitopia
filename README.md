# Whitopia.jp 店鋪開業信息爬蟲

這是一個專門用於抓取和分析 Whitopia.jp 網站店鋪開業信息的爬蟲系統。

## 🚀 快速開始

### 1. 系統要求
- Python 3.7 或更高版本
- 穩定的網絡連接

### 2. 安裝依賴
```bash
# 使用系統包管理器安裝（推薦）
sudo apt install python3-requests python3-bs4 python3-lxml

# 或使用pip安裝（如果允許）
pip install -r requirements.txt
```

### 3. 驗證安裝
```bash
python3 test_scraper.py
```
如果看到 "🎉 所有測試通過！爬蟲已準備就緒"，表示系統已準備好使用。

## 📋 使用方法

### 基本使用

#### 1. 運行爬蟲（抓取最新數據）
```bash
python3 whitopia_scraper.py
```
這會：
- 訪問 https://www.whitopia.jp
- 抓取お知らせ信息
- 識別店鋪開業相關內容
- 生成 `whitopia_news.json` 文件

#### 2. 分析數據
```bash
python3 whitopia_improved_analyzer.py
```
這會：
- 讀取爬蟲數據
- 提取店鋪名稱、開業日期、地區信息
- 生成詳細的分析報告
- 保存結果到 `whitopia_detailed_analysis.json`

### 高級使用

#### 自動化運行
```bash
# 一次性運行完整流程
python3 whitopia_scraper.py && python3 whitopia_improved_analyzer.py
```

#### 定期監控（例如每天運行一次）
```bash
# 添加到 crontab
0 9 * * * cd /path/to/scraper && python3 whitopia_scraper.py && python3 whitopia_improved_analyzer.py
```

## 📁 文件說明

### 核心文件
- `whitopia_scraper.py` - 主要爬蟲腳本
- `whitopia_improved_analyzer.py` - 數據分析腳本
- `test_scraper.py` - 測試腳本
- `requirements.txt` - 依賴列表

### 輸出文件
- `whitopia_news.json` - 原始爬蟲數據
- `whitopia_detailed_analysis.json` - 詳細分析結果
- `whitopia_report.md` - 人類可讀的分析報告

## 🔍 輸出示例

### 控制台輸出
```
======================================================================
🏪 Whitopia.jp 店鋪開業信息詳細分析
======================================================================
📊 分析時間: 2025年07月29日 03:15:07
📅 數據抓取時間: 2025-07-29T03:13:53.594581
📈 總共找到項目: 3 個
🏬 店鋪相關項目: 3 個

🗓️ 店鋪開業時間表:
======================================================================
🏪 1. ホワイトピア美野島店
   📅 開業日期: 2025年07月07日 (月)
   📍 所在地區: 福岡県
   🔍 關鍵詞: OPEN
   🔗 URL: https://www.whitopia.jp
```

### JSON 輸出結構
```json
{
  "analysis_time": "2025-07-29T03:15:07.123456",
  "total_stores": 3,
  "store_openings": [
    {
      "store_name": "ホワイトピア美野島店",
      "prefecture": "福岡県",
      "date": "2025-07-07",
      "match_keyword": "OPEN"
    }
  ],
  "monthly_stats": {
    "2025-07": 1,
    "2025-06": 2
  },
  "prefecture_stats": {
    "香川県": 2,
    "福岡県": 1
  }
}
```

## 🛠️ 自定義配置

### 修改目標網站
在 `whitopia_scraper.py` 中修改：
```python
self.base_url = "https://your-target-website.com"
```

### 調整關鍵詞
在 `filter_store_opening_news` 方法中修改：
```python
store_keywords = [
    '開店', '開業', 'オープン', 'OPEN', 'open', '新店',
    # 添加您需要的關鍵詞
]
```

### 修改請求頻率
在 `get_page` 方法中調整：
```python
time.sleep(2)  # 增加延遲時間
```

## 🔧 故障排除

### 常見問題

#### 1. 網絡連接失敗
```bash
# 檢查網絡連接
ping www.whitopia.jp

# 檢查DNS解析
nslookup www.whitopia.jp
```

#### 2. 依賴安裝失敗
```bash
# 更新包管理器
sudo apt update

# 重新安裝依賴
sudo apt install python3-requests python3-bs4 python3-lxml
```

#### 3. 權限問題
```bash
# 確保文件可執行
chmod +x whitopia_scraper.py
chmod +x whitopia_improved_analyzer.py
chmod +x test_scraper.py
```

#### 4. 數據格式變化
如果網站結構發生變化，可能需要更新正則表達式模式：
- 檢查 `extract_store_info` 方法中的模式
- 調整 `scrape_news_list` 方法中的選擇器

### 調試模式
```bash
# 運行時顯示詳細錯誤信息
python3 -u whitopia_scraper.py 2>&1 | tee scraper.log
```

## 📊 性能優化

### 提高抓取速度
- 調整 `timeout` 參數
- 使用併發請求（謹慎使用）
- 緩存已處理的數據

### 減少資源使用
- 限制解析的內容範圍
- 定期清理舊的輸出文件
- 壓縮存儲的JSON數據

## 🔒 合規性說明

- 本爬蟲遵循 robots.txt 規範
- 使用合理的請求頻率，避免對服務器造成負擔
- 僅抓取公開可訪問的信息
- 建議在使用前檢查網站的使用條款

## 📞 支持

如果遇到問題：
1. 首先運行 `python3 test_scraper.py` 進行診斷
2. 檢查網絡連接和依賴安裝
3. 查看生成的日誌文件
4. 檢查是否需要更新代碼以適應網站變化

## 📈 未來改進

- 添加更多數據源
- 實現實時監控功能
- 添加郵件通知功能
- 支持更多輸出格式（CSV、Excel等）
- 添加圖形化界面