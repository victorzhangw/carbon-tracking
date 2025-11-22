import sqlite3, random
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent
LOG_DIR = BASE / 'logs'
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = Path('data/databases/carbon_tracking.db')

PILOT_START = datetime(2025,2,1)
PILOT_END = datetime(2025,10,31)


def write_log(path: Path, lines):
    path.write_text("\n".join(lines)+"\n", encoding='utf-8')


def q(conn, sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchall()


def load_db_distributions(conn):
    # 基於資料庫推估分布：交通占比、平均距離、每工每日訪視量
    transport = q(conn, "SELECT transport_type, COUNT(*), AVG(distance) FROM visit_records GROUP BY transport_type")
    total = sum(r[1] for r in transport) or 1
    transport_weights = {r[0]: r[1]/total for r in transport} or {'機車':0.65,'汽車':0.3,'大眾運輸':0.05}
    avg_distance = sum((r[1]* (r[2] or 10)) for r in transport)/total if total else 10

    # 依社工訪視強度
    by_worker = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*) FROM visit_records GROUP BY 1,2")
    worker_weights = {}
    tw = sum(r[2] for r in by_worker) or 1
    for wid, wname, cnt in by_worker:
        worker_weights[(wid, wname)] = cnt/tw
    if not worker_weights:
        # 預設 15 名常見社工
        sample_workers = [
            ('SW001','王小明'),('SW002','李小華'),('SW003','張小美'),('SW004','吳宜靜'),('SW005','林怡君'),
            ('SW006','黃小玲'),('SW007','吳小文'),('SW008','劉小雯'),('SW009','鄭小傑'),('SW010','謝小慧'),
            ('SW011','王建宏'),('SW012','劉俊傑'),('SW013','張志偉'),('SW014','陳冠廷'),('SW015','林哲瑋')
        ]
        worker_weights = {w:1/len(sample_workers) for w in sample_workers}

    # 估計每月工作日每日訪視量分布（以資料庫按月總量平均）
    by_month = q(conn, "SELECT strftime('%Y-%m', visit_date) ym, COUNT(*) FROM visit_records GROUP BY ym")
    month_avg = int(sum(r[1] for r in by_month)/len(by_month)) if by_month else 8000

    return transport_weights, avg_distance, worker_weights, month_avg


def generate_modeled_pilot(conn):
    # 以資料庫分布建構試營運期（2-10月）的模擬數據，加入合理抖動
    tw, avg_dist, ww, month_avg = load_db_distributions(conn)

    days = []
    d = PILOT_START
    while d <= PILOT_END:
        if d.weekday() < 5:  # 工作日
            days.append(d)
        d += timedelta(days=1)

    # 每個月的目標量（稍有起伏）
    month_targets = {}
    cur = PILOT_START
    while cur <= PILOT_END:
        ym = (cur.year, cur.month)
        if ym not in month_targets:
            jitter = random.randint(-800, 800)
            month_targets[ym] = max(3000, month_avg + jitter)
        cur += timedelta(days=31-cur.day)
        cur = cur.replace(day=1)

    # 交通係數
    coeff = {t:q(conn, "SELECT coefficient FROM emission_coefficients WHERE transport_type=?", (t,))[0][0] if q(conn, "SELECT coefficient FROM emission_coefficients WHERE transport_type=?", (t,)) else {'機車':0.063,'汽車':0.2171,'大眾運輸':0.0573}[t] for t in ['機車','汽車','大眾運輸']}

    # 開始生成
    by_worker = {}
    by_month = {}
    by_transport = {t:[0,0.0,0.0] for t in coeff.keys()}  # visits, km, kg

    for d in days:
        ym = f"{d.year}-{d.month:02d}"
        # 當月目標均攤到工作日，再加當日抖動
        workdays_in_month = sum(1 for x in days if x.year==d.year and x.month==d.month)
        base = month_targets[(d.year,d.month)]//max(1,workdays_in_month)
        today_visits = max(50, int(random.gauss(base, base*0.15)))

        # 每筆訪視：指派社工、交通、距離（依平均距離帶抖動）
        ww_items = list(ww.items())
        for _ in range(today_visits):
            (wid,wname), wprob = random.choices(ww_items, weights=[w[1] for w in ww_items])[0]
            t = random.choices(list(tw.keys()), weights=list(tw.values()))[0]
            dist = max(0.5, random.gauss(avg_dist, avg_dist*0.4))
            kg = dist*coeff[t]

            # 累加社工
            agg = by_worker.setdefault((wid,wname), [0,0.0,0.0])
            agg[0]+=1; agg[1]+=dist; agg[2]+=kg
            # 累加月份
            agg2 = by_month.setdefault(ym, [0,0.0,0.0])
            agg2[0]+=1; agg2[1]+=dist; agg2[2]+=kg
            # 累加交通
            by_transport[t][0]+=1; by_transport[t][1]+=dist; by_transport[t][2]+=kg

    # 輸出
    total_visits = sum(v[0] for v in by_worker.values())
    total_km = sum(v[1] for v in by_worker.values())
    total_kg = sum(v[2] for v in by_worker.values())

    lines = []
    lines.append('CARBON EMISSIONS LOG (PILOT PERIOD, MODELED FROM DB DISTRIBUTIONS)')
    lines.append('口徑說明：本檔案基於資料庫分布（社工權重、交通占比、平均距離）於 2025/02–10 建構模擬數據，用於呈現真實世界變化特徵；非實際資料。')
    lines.append('欄位中文說明：visits=訪視次數；total_km=行駛里程(公里)；total_kg_co2e=碳排(公斤二氧化碳當量)')
    lines.append(f'PERIOD: {PILOT_START.date()} to {PILOT_END.date()}')
    lines.append(f'TOTAL_VISITS: {int(total_visits)}')
    lines.append(f'TOTAL_KM: {total_km:.1f}')
    lines.append(f'TOTAL_KG_CO2E: {total_kg:.1f}')
    lines.append('')
    lines.append('BY_WORKER (TOP 15):')
    lines.append('worker_id,worker_name,visits,total_km,total_kg_co2e')
    for (wid,wname), v in sorted(by_worker.items(), key=lambda x: -x[1][2])[:15]:
        lines.append(f"{wid},{wname},{v[0]},{v[1]:.1f},{v[2]:.1f}")
    lines.append('')
    lines.append('BY_MONTH:')
    lines.append('year_month,visits,total_km,total_kg_co2e')
    for ym, v in sorted(by_month.items()):
        lines.append(f"{ym},{v[0]},{v[1]:.1f},{v[2]:.1f}")
    lines.append('')
    lines.append('BY_TRANSPORT:')
    lines.append('transport,visits,total_km,total_kg_co2e')
    for t, v in by_transport.items():
        lines.append(f"{t},{v[0]},{v[1]:.1f},{v[2]:.1f}")

    write_log(LOG_DIR / 'pilot_modeled_carbon_emissions.log', lines)


def gen_db_actual_logs():
    if not DB_PATH.exists():
        return 'no_db'
    conn = sqlite3.connect(str(DB_PATH))
    # 期間
    res = q(conn, "SELECT MIN(visit_date), MAX(visit_date) FROM visit_records")
    min_date, max_date = res[0] if res else (None, None)
    if not min_date:
        return 'no_records'

    # by worker
    by_worker = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1,2 ORDER BY 5 DESC")
    # by month
    by_month = q(conn, "SELECT strftime('%Y-%m', visit_date), COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1 ORDER BY 1")
    # by transport
    by_transport = q(conn, "SELECT transport_type, COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1 ORDER BY 4 DESC")
    conn.close()

    tv = sum(r[2] for r in by_worker) if by_worker else 0
    tk = sum(r[3] for r in by_worker) if by_worker else 0
    tg = sum(r[4] for r in by_worker) if by_worker else 0

    lines = []
    lines.append('CARBON EMISSIONS LOG (DB ACTUAL)')
    lines.append('口徑說明：本檔案完全依據資料庫 visit_records 實際數據彙整。')
    lines.append('欄位中文說明：visits=訪視次數；total_km=行駛里程(公里)；total_kg_co2e=碳排(公斤二氧化碳當量)')
    lines.append(f'PERIOD: {min_date} to {max_date}')
    lines.append(f'TOTAL_VISITS: {int(tv)}')
    lines.append(f'TOTAL_KM: {tk}')
    lines.append(f'TOTAL_KG_CO2E: {tg}')
    lines.append('')
    lines.append('BY_WORKER (TOP 20):')
    lines.append('worker_id,worker_name,visits,total_km,total_kg_co2e')
    for row in by_worker[:20]:
        lines.append(','.join(str(x) for x in row))
    lines.append('')
    lines.append('BY_MONTH:')
    lines.append('year_month,visits,total_km,total_kg_co2e')
    for row in by_month:
        lines.append(','.join(str(x) for x in row))
    lines.append('')
    lines.append('BY_TRANSPORT:')
    lines.append('transport,visits,total_km,total_kg_co2e')
    for row in by_transport:
        lines.append(','.join(str(x) for x in row))

    write_log(LOG_DIR / 'db_actual_carbon_emissions.log', lines)
    return 'ok'


def main():
    status = gen_db_actual_logs()
    if status != 'no_db':
        try:
            conn = sqlite3.connect(str(DB_PATH))
            generate_modeled_pilot(conn)
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    main()
