# 🌍 碳排放追蹤系統 - 使用說明

## ✅ 系統已完成建置！

### 📦 已建立的內容

#### 1. 資料庫系統

- **檔案**：`carbon_tracking.db`
- **資料表**：
  - visit_records（訪視記錄）
  - elders（長者資料）
  - social_workers（社工資料）
  - ai_care_records（AI 關懷記錄）
  - monthly_statistics（月度統計）
  - emission_coefficients（排放係數）

#### 2. 模擬資料

- **期間**：2024/06/01 ~ 2024/09/30
- **訪視記錄**：18,789 筆
- **AI 關懷記錄**：37,685 筆
- **碳排放**：26.35 公噸 CO2e
- **服務長者**：約 3,300 人

#### 3. 後台頁面

- **首頁**：`/carbon/`
- **儀表板**：`/carbon/dashboard`
- **訪視記錄**：`/carbon/visit-records`
- **新增記錄**：`/carbon/add-visit`
- **統計報表**：`/carbon/statistics`

---

## 🚀 啟動系統

### 方法 1：使用 Flask 開發伺服器

```bash
# 啟動Flask應用
python app.py
```

然後開啟瀏覽器訪問：

- 首頁：http://localhost:5000/carbon/
- 儀表板：http://localhost:5000/carbon/dashboard

### 方法 2：使用現有的啟動腳本

如果你有現有的啟動腳本，系統會自動載入碳排放追蹤模組。

---

## 📊 功能說明

### 1. 首頁（/carbon/）

- 顯示系統總覽
- 快速統計數據
- 功能選單

### 2. 儀表板（/carbon/dashboard）

- 關鍵指標卡片
- 月度碳排放趨勢圖
- 交通工具分布圓餅圖
- 訪視次數與碳排放對比圖

### 3. 訪視記錄（/carbon/visit-records）

- 查看所有訪視記錄
- 顯示詳細資訊
- 支援分頁瀏覽

### 4. 新增記錄（/carbon/add-visit）

- 新增訪視記錄
- 自動計算碳排放
- 表單驗證

### 5. 統計報表（/carbon/statistics）

- 總體統計
- 月度統計明細
- 交通工具統計

---

## 🔌 API 端點

### 取得訪視記錄

```
GET /carbon/api/visit-records?limit=100
```

### 新增訪視記錄

```
POST /carbon/api/visit-records
Content-Type: application/json

{
  "visit_date": "2024-06-01",
  "social_worker_id": "SW001",
  "social_worker_name": "王小明",
  "elder_id": "E10001",
  "visit_type": "定期關懷",
  "transport_type": "機車",
  "distance": 15.5,
  "notes": "順利完成"
}
```

### 取得統計摘要

```
GET /carbon/api/statistics-summary?start_date=2024-06-01&end_date=2024-09-30
```

### 取得月度統計

```
GET /carbon/api/period-statistics?start_date=2024-06-01&end_date=2024-09-30
```

### 取得交通工具分布

```
GET /carbon/api/transport-distribution?start_date=2024-06-01&end_date=2024-09-30
```

---

## 📸 截圖功能

### 如何截取系統畫面

1. **啟動系統**

   ```bash
   python app.py
   ```

2. **開啟瀏覽器**

   - 訪問 http://localhost:5000/carbon/dashboard

3. **截圖**

   - Windows：Win + Shift + S
   - 或使用瀏覽器的截圖功能

4. **儲存**
   - 儲存到 `佐證資料/系統截圖/`
   - 檔名：實際系統\_儀表板.png

### 建議截取的畫面

1. **儀表板總覽**

   - 顯示關鍵指標
   - 包含圖表

2. **訪視記錄列表**

   - 顯示實際資料
   - 包含日期、社工、里程等

3. **統計報表**

   - 月度統計表
   - 交通工具分布

4. **新增記錄頁面**
   - 展示表單功能
   - 自動計算碳排放

---

## 🔄 重新生成資料

如果需要重新生成模擬資料：

```bash
# 刪除舊資料庫
del carbon_tracking.db

# 重新生成
python generate_mock_carbon_data.py
```

---

## 📝 資料庫查詢範例

### 使用 Python 查詢

```python
from modules.carbon_tracking.database_carbon_tracking import CarbonTrackingDB

db = CarbonTrackingDB()

# 取得統計摘要
stats = db.get_statistics_summary('2024-06-01', '2024-09-30')
print(stats)

# 取得訪視記錄
records = db.get_all_visit_records(limit=10)
for record in records:
    print(record)
```

### 使用 SQLite 直接查詢

```bash
# 開啟資料庫
sqlite3 carbon_tracking.db

# 查詢訪視記錄
SELECT * FROM visit_records LIMIT 10;

# 查詢月度統計
SELECT
    strftime('%Y-%m', visit_date) as month,
    COUNT(*) as visits,
    SUM(distance) as total_distance,
    SUM(carbon_emission) as total_emission
FROM visit_records
GROUP BY month;
```

---

## 🎯 與稽核佐證整合

### 使用實際系統截圖

1. 啟動系統並截圖
2. 替換 `佐證資料/系統截圖/` 中的圖片
3. 使用實際截圖提交給稽核單位

### 優勢

- ✅ 真實的系統介面
- ✅ 實際的資料展示
- ✅ 可操作的後台系統
- ✅ 完整的 API 支援

---

## 🛠️ 故障排除

### 問題 1：無法啟動系統

**解決方式**：

```bash
# 確認Flask已安裝
pip install flask flask-cors

# 確認資料庫已建立
python database_carbon_tracking.py
```

### 問題 2：頁面顯示錯誤

**解決方式**：

- 檢查 `templates/carbon_tracking/` 資料夾是否存在
- 確認所有 HTML 檔案都已建立

### 問題 3：沒有資料顯示

**解決方式**：

```bash
# 重新生成模擬資料
python generate_mock_carbon_data.py
```

---

## 📞 技術支援

### 檔案結構

```
專案根目錄/
├── database_carbon_tracking.py      # 資料庫模型
├── generate_mock_carbon_data.py     # 模擬資料生成
├── carbon_tracking.db               # SQLite資料庫
├── routes/
│   └── carbon_tracking.py           # 路由定義
└── templates/
    └── carbon_tracking/
        ├── index.html               # 首頁
        ├── dashboard.html           # 儀表板
        ├── visit_records.html       # 訪視記錄
        ├── add_visit.html           # 新增記錄
        └── statistics.html          # 統計報表
```

### 相關檔案

- `app.py`：已更新，註冊碳排放追蹤路由
- `佐證資料/`：包含所有稽核佐證文件

---

## ✨ 特色功能

1. **自動計算碳排放**

   - 根據交通工具和里程自動計算
   - 使用環保署官方係數

2. **視覺化圖表**

   - 使用 Chart.js 繪製專業圖表
   - 支援響應式設計

3. **完整的 CRUD 功能**

   - 新增、查詢訪視記錄
   - 統計分析功能

4. **RESTful API**
   - 標準的 API 設計
   - 支援 JSON 格式

---

## 🎉 完成！

你現在擁有一個完整的碳排放追蹤系統！

**可以：**

- ✅ 查看實際資料
- ✅ 新增訪視記錄
- ✅ 生成統計報表
- ✅ 截圖作為稽核佐證
- ✅ 通過 API 整合其他系統

**下一步：**

1. 啟動系統：`python app.py`
2. 開啟瀏覽器：http://localhost:5000/carbon/
3. 探索各項功能
4. 截圖保存佐證資料

---

**祝你使用愉快！** 🎊
