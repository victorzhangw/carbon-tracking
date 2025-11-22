import sqlite3, random, math
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent
LOG_DIR = BASE / 'logs'
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = Path('data/databases/carbon_tracking.db')

PILOT_START = datetime(2025,2,1)
PILOT_END = datetime(2025,10,31)

# 參考係數（若資料庫無對應表）
EMISSION_COEFF = {'機車':0.063,'汽車':0.2171,'大眾運輸':0.0573}


def write_log(path: Path, lines):
    path.write_text("\n".join(lines)+"\n", encoding='utf-8')

def q(conn, sql, params=()):
    cur = conn.cursor(); cur.execute(sql, params); return cur.fetchall()


def get_coeff(conn, t):
    try:
        r = q(conn, "SELECT coefficient FROM emission_coefficients WHERE transport_type=?", (t,))
        if r:
            return float(r[0][0])
    except Exception:
        pass
    return EMISSION_COEFF.get(t, 0.1)


def gen_db_actual():
    if not DB_PATH.exists():
        write_log(LOG_DIR / 'db_actual_carbon_emissions.log', [
            '碳排放日誌（資料庫實際彙整）',
            '資料來源：data/databases/carbon_tracking.db / 表：visit_records',
            '狀態：找不到資料庫檔案'
        ])
        return
    conn = sqlite3.connect(str(DB_PATH))

    # 基本期間
    res = q(conn, "SELECT MIN(visit_date), MAX(visit_date) FROM visit_records")
    min_date, max_date = res[0] if res else (None, None)

    # 指標彙總
    by_worker = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1,2 ORDER BY 5 DESC")
    by_month = q(conn, "SELECT strftime('%Y-%m', visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 1")
    by_transport = q(conn, "SELECT transport_type, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 4 DESC")
    by_day = q(conn, "SELECT date(visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 1 DESC LIMIT 30")

    # 異常偵測：單次距離>50km 前50筆
    long_trips = q(conn, "SELECT visit_date, social_worker_id, social_worker_name, transport_type, distance, COALESCE(carbon_emission,0) FROM visit_records WHERE distance > 50 ORDER BY distance DESC LIMIT 50")

    # 異常偵測：單人單日訪視過高（> 平均+3σ）
    per_day = q(conn, "SELECT social_worker_id, social_worker_name, date(visit_date), COUNT(*) FROM visit_records GROUP BY 1,2,3")
    # 統計每位社工的日訪視頻率
    from collections import defaultdict
    worker_counts = defaultdict(list)
    for wid, wname, d, c in per_day:
        worker_counts[(wid,wname)].append(c)
    high_days = []
    for (wid,wname), arr in worker_counts.items():
        if not arr: continue
        mean = sum(arr)/len(arr)
        var = sum((x-mean)**2 for x in arr)/len(arr)
        sd = math.sqrt(var)
        thr = mean + 3*sd
        for (wwid, wwn, d, c) in per_day:
            if wwid==wid and wwn==wname and c>thr and c>=10:  # 至少10次視為高負載
                high_days.append((d, wid, wname, c, round(mean,2), round(sd,2), round(thr,2)))
    # 去重並取前50
    seen = set(); filtered_high = []
    for r in high_days:
        key = (r[0], r[1])
        if key not in seen:
            seen.add(key); filtered_high.append(r)
    filtered_high.sort(key=lambda x: (-x[3], x[0]))
    filtered_high = filtered_high[:50]

    # 總計
    tv = sum(r[2] for r in by_worker) if by_worker else 0
    tk = sum(r[3] for r in by_worker) if by_worker else 0.0
    tg = sum(r[4] for r in by_worker) if by_worker else 0.0

    L = []
    L.append('碳排放日誌（資料庫實際彙整）')
    L.append('資料來源：data/databases/carbon_tracking.db / 表：visit_records')
    L.append('欄位中文說明：訪視次數=visits；行駛里程(公里)=total_km；碳排(公斤CO2e)=total_kg_co2e')
    L.append(f'統計期間：{min_date} 至 {max_date}')
    L.append(f'總訪視次數：{int(tv)}')
    L.append(f'總里程(公里)：{tk:.1f}')
    L.append(f'總碳排(公斤CO2e)：{tg:.1f}')
    L.append('')
    L.append('依社工彙總（前20名）')
    L.append('工號,姓名,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for r in by_worker[:20]:
        L.append(f'{r[0]},{r[1]},{int(r[2])},{float(r[3]):.1f},{float(r[4]):.1f}')
    L.append('')
    L.append('依月份彙總')
    L.append('年月,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for r in by_month:
        L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    L.append('')
    L.append('依交通工具彙總')
    L.append('交通工具,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for r in by_transport:
        L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    L.append('')
    L.append('最近30日彙總（依日）')
    L.append('日期,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for r in by_day:
        L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    L.append('')
    L.append('異常偵測：單次距離>50公里（前50）')
    L.append('日期,工號,姓名,交通工具,距離(公里),碳排(公斤CO2e)')
    for r in long_trips:
        L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{float(r[4]):.1f},{float(r[5]):.1f}')
    L.append('')
    L.append('異常偵測：單人單日訪視過高（> 平均+3σ，且至少10次；前50）')
    L.append('日期,工號,姓名,當日訪視數,個人日均值,日標準差,門檻值')
    for r in filtered_high:
        L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]}')

    write_log(LOG_DIR / 'db_actual_carbon_emissions.log', L)
    conn.close()


def gen_pilot_modeled():
    # 基於資料庫分布生成 2025/02–10 模型化數據
    conn = None
    if DB_PATH.exists():
        conn = sqlite3.connect(str(DB_PATH))
        workers = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*) FROM visit_records GROUP BY 1,2 ORDER BY 3 DESC LIMIT 20")
        total = sum(r[2] for r in workers) or 1
        worker_weights = [ (r[0], r[1], r[2]/total) for r in workers ] or []
        transports = q(conn, "SELECT transport_type, COUNT(*), AVG(distance) FROM visit_records GROUP BY 1 ORDER BY 2 DESC")
        t_total = sum(r[1] for r in transports) or 1
        transport_weights = [ (r[0], r[1]/t_total, (r[2] or 12.0)) for r in transports ] or []
    else:
        worker_weights = []
        transports = []

    if not worker_weights:
        worker_weights = [
            ('SW001','王小明',0.1),('SW002','李小華',0.1),('SW003','張小美',0.1),('SW004','吳宜靜',0.1),('SW005','林怡君',0.1),
            ('SW006','黃小玲',0.06),('SW007','吳小文',0.06),('SW008','劉小雯',0.06),('SW009','鄭小傑',0.06),('SW010','謝小慧',0.06),
            ('SW011','王建宏',0.04),('SW012','劉俊傑',0.04),('SW013','張志偉',0.04),('SW014','陳冠廷',0.04),('SW015','林哲瑋',0.04)
        ]
    if not transport_weights:
        transport_weights = [('機車',0.65,12.0),('汽車',0.30,18.0),('大眾運輸',0.05,10.0)]

    # 準備每日
    days = []
    d = PILOT_START
    while d <= PILOT_END:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)

    # 每月目標（波動）
    month_targets = {}
    cur = PILOT_START
    while cur <= PILOT_END:
        ym = (cur.year, cur.month)
        if ym not in month_targets:
            base = 1200
            jitter = random.randint(-200, 200)
            month_targets[ym] = max(600, base + jitter)
        # next month
        next_month = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
        cur = next_month

    # 累計容器
    from collections import defaultdict
    by_worker = defaultdict(lambda:[0,0.0,0.0])
    by_month = defaultdict(lambda:[0,0.0,0.0])
    by_transport = defaultdict(lambda:[0,0.0,0.0])
    by_day = defaultdict(lambda:[0,0.0,0.0])

    # 係數表
    def coeff_of(t):
        if conn:
            try:
                return get_coeff(conn, t)
            except Exception:
                return EMISSION_COEFF.get(t,0.1)
        return EMISSION_COEFF.get(t,0.1)

    # 生成
    for d in days:
        ym = (d.year, d.month)
        workdays_count = sum(1 for x in days if x.year==d.year and x.month==d.month)
        base = month_targets[ym]//max(1,workdays_count)
        today = max(30, int(random.gauss(base, base*0.18)))
        for _ in range(today):
            wid,wname,p = random.choices(worker_weights, weights=[w[2] for w in worker_weights])[0]
            t, tw, avg_dist = random.choices(transport_weights, weights=[x[1] for x in transport_weights])[0]
            dist = max(0.6, random.gauss(avg_dist, avg_dist*0.4))
            kg = dist * coeff_of(t)
            # 累加
            by_worker[(wid,wname)][0]+=1; by_worker[(wid,wname)][1]+=dist; by_worker[(wid,wname)][2]+=kg
            keym = f"{d.year}-{d.month:02d}"
            by_month[keym][0]+=1; by_month[keym][1]+=dist; by_month[keym][2]+=kg
            by_transport[t][0]+=1; by_transport[t][1]+=dist; by_transport[t][2]+=kg
            keyd = d.strftime('%Y-%m-%d')
            by_day[keyd][0]+=1; by_day[keyd][1]+=dist; by_day[keyd][2]+=kg

    total_v = sum(v[0] for v in by_worker.values())
    total_km = sum(v[1] for v in by_worker.values())
    total_kg = sum(v[2] for v in by_worker.values())

    L = []
    L.append('碳排放日誌（試營運期模型化數據）')
    L.append('資料來源：依資料庫分布（社工權重、交通占比、距離）建模，期間 2025/02–10；非實際資料，僅用於呈現趨勢特徵')
    L.append('欄位中文說明：訪視次數=visits；行駛里程(公里)=total_km；碳排(公斤CO2e)=total_kg_co2e')
    L.append(f'統計期間：{PILOT_START.date()} 至 {PILOT_END.date()}')
    L.append(f'總訪視次數：{int(total_v)}')
    L.append(f'總里程(公里)：{total_km:.1f}')
    L.append(f'總碳排(公斤CO2e)：{total_kg:.1f}')
    L.append('')
    L.append('依社工彙總（前15名）')
    L.append('工號,姓名,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for (wid,wname), v in sorted(by_worker.items(), key=lambda x: -x[1][2])[:15]:
        L.append(f'{wid},{wname},{int(v[0])},{v[1]:.1f},{v[2]:.1f}')
    L.append('')
    L.append('依月份彙總')
    L.append('年月,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for ym, v in sorted(by_month.items()):
        L.append(f'{ym},{int(v[0])},{v[1]:.1f},{v[2]:.1f}')
    L.append('')
    L.append('依交通工具彙總')
    L.append('交通工具,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for t, v in by_transport.items():
        L.append(f'{t},{int(v[0])},{v[1]:.1f},{v[2]:.1f}')
    L.append('')
    L.append('最近30日彙總（依日，模型化）')
    L.append('日期,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for d, v in sorted(by_day.items())[-30:]:
        L.append(f'{d},{int(v[0])},{v[1]:.1f},{v[2]:.1f}')

    write_log(LOG_DIR / 'pilot_modeled_carbon_emissions.log', L)
    if conn:
        conn.close()

if __name__ == '__main__':
    gen_db_actual()
    gen_pilot_modeled()
