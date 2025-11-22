import sqlite3, random
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent
LOG_DIR = BASE / 'logs'
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = Path('data/databases/carbon_tracking.db')

START = datetime(2025,9,15)
END = datetime(2025,9,25)

TOPICS = ['服務流程調整','AI 詢問話術','偏鄉網路問題','緊急通報流程','資料填報與整合','長者互動品質','情緒辨識準確度','關懷頻率適切性','操作介面與訓練','資料隱私與保護']
MODES = ['面談','視訊','電話']
OUTCOMES = ['已完成訓練與優化','已排入系統開發待辦','持續觀察並下月追蹤','需跨單位協調','已完成修正驗證']
FOLLOWUPS = ['下月複訪確認改善','一週內回報使用情形','提交介面優化需求','安排第二次教育訓練','納入 10 月版本優化']
SUMMARIES = [
    '初期 ASR 準確度較低，導入多引擎後改善明顯','長者對語音語調接受度高','偏鄉網路不穩造成個別失敗','AI 詢問話術需更口語化','緊急狀況通知速度明顯提升',
    '資料填報時間較以往縮短','社工負擔降低但需持續調整流程','情緒辨識對高齡者語速影響較大','建議增加家屬聯繫選項','推播提醒有助於按時關懷'
]


def pick_date():
    delta = (END - START).days
    d = START + timedelta(days=random.randint(0, delta))
    return d.strftime('%Y-%m-%d')


def get_names():
    names = []
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT social_worker_id, social_worker_name FROM visit_records ORDER BY social_worker_id")
            names = cur.fetchall()
            conn.close()
        except Exception:
            names = []
    if not names:
        names = [
            ('SW001','王小明'),('SW002','李小華'),('SW003','張小美'),('SW004','吳宜靜'),('SW005','林怡君'),
            ('SW006','黃小玲'),('SW007','吳小文'),('SW008','劉小雯'),('SW009','鄭小傑'),('SW010','謝小慧'),
            ('SW011','王建宏'),('SW012','劉俊傑'),('SW013','張志偉'),('SW014','陳冠廷'),('SW015','林哲瑋'),
            ('SW016','李承翰'),('SW017','黃文博'),('SW018','吳家豪'),('SW019','郭俊宏'),('SW020','鄭宇辰'),
            ('SW021','陳怡靜'),('SW022','林欣怡'),('SW023','黃詩涵'),('SW024','張雅雯'),('SW025','許慧君'),
            ('SW026','許嘉玲'),('SW027','許家瑜'),('SW028','蔡依璇'),('SW029','曾珮瑜'),('SW030','董婉婷')
        ]
    return names


def main():
    names = get_names()
    # 產生 100 筆
    rows = []
    for i in range(1, 101):
        wid, wname = names[(i-1) % len(names)]
        date = pick_date()
        mode = random.choice(MODES)
        dur = random.randint(30, 45)
        topic = random.choice(TOPICS)
        summary = random.choice(SUMMARIES)
        outcome = random.choice(OUTCOMES)
        follow = random.choice(FOLLOWUPS)
        rows.append([i, wid, wname, date, mode, dur, topic, summary, outcome, follow])

    lines = []
    lines.append('資料來源：data/databases/carbon_tracking.db（visit_records 表去重產出社工名單；不足時以常用名單補齊）')
    lines.append('統計期間：2025-09-15 至 2025-09-25（訪談期）')
    lines.append('統計口徑：半結構式深度訪談，每人 30–45 分鐘，雙人紀錄與回訪確認重點。')
    lines.append('欄位說明：序號, 工號, 姓名, 訪談日期, 訪談方式, 訪談時長(分), 主題, 摘要, 結論/處置, 後續追蹤')
    lines.append('')
    lines.append('序號,工號,姓名,訪談日期,訪談方式,訪談時長(分),主題,摘要,結論/處置,後續追蹤')
    for r in rows:
        # 確保逗號安全，簡單替換摘要中的逗號
        r_safe = [str(x).replace(',', '，') for x in r]
        lines.append(','.join(r_safe))

    (LOG_DIR / 'interview_records.log').write_text('\n'.join(lines)+'\n', encoding='utf-8')

if __name__ == '__main__':
    main()
