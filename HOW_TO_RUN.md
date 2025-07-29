# 🚀 Whitopia.jp 爬蟲運行指南

## 📝 簡單運行方法

### 方法一：使用自動腳本（推薦）
```bash
./run_scraper.sh
```

### 方法二：手動分步運行
```bash
# 第一步：運行爬蟲
python3 whitopia_scraper.py

# 第二步：分析數據
python3 whitopia_improved_analyzer.py
```

### 方法三：測試系統
```bash
python3 test_scraper.py
```

## 📁 結果文件位置

運行完成後，結果會保存在以下文件中：

### 🎯 主要結果文件

| 文件名 | 說明 | 用途 |
|--------|------|------|
| `whitopia_detailed_analysis.json` | 詳細分析結果 | 程序讀取、數據分析 |
| `whitopia_report.md` | 人類可讀報告 | 閱讀、分享 |
| `whitopia_news.json` | 原始爬蟲數據 | 備份、調試 |

### 📊 結果內容示例

**找到的店鋪開業信息：**
1. **ホワイトピア美野島店** - 2025年07月07日（福岡県）
2. **ホワイトピア高松伏石店** - 2025年06月26日（香川県）
3. **ホワイトピア高松鶴市店** - 2025年06月09日（香川県）

## 🔍 如何查看結果

### 查看詳細報告
```bash
cat whitopia_report.md
```

### 查看JSON數據
```bash
cat whitopia_detailed_analysis.json | python3 -m json.tool
```

### 查看原始數據
```bash
cat whitopia_news.json
```

## 📋 運行檢查清單

在運行前請確認：

- [ ] ✅ Python 3.7+ 已安裝
- [ ] ✅ 網絡連接正常
- [ ] ✅ 依賴庫已安裝 (`python3-requests`, `python3-bs4`, `python3-lxml`)
- [ ] ✅ 有寫入權限（用於保存結果文件）

## 🆘 常見問題

### Q: 如何知道爬蟲是否成功運行？
A: 看到以下訊息表示成功：
```
🎉 爬蟲運行完成！結果已保存到以上文件中。
```

### Q: 結果文件在哪裡？
A: 在與腳本相同的目錄下，檔名以 `whitopia_` 開頭的 `.json` 和 `.md` 文件。

### Q: 如何定期運行？
A: 可以設置 cron job：
```bash
# 每天上午9點運行
0 9 * * * cd /path/to/scraper && ./run_scraper.sh
```

### Q: 運行失敗怎麼辦？
A: 首先運行測試：
```bash
python3 test_scraper.py
```
根據測試結果進行相應的修復。

## 🎯 快速開始

**只需要記住這一個命令：**
```bash
./run_scraper.sh
```

運行後查看生成的文件即可！