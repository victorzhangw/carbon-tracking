import sqlite3, random
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
LOG_DIR = BASE / 'logs'
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = Path('data/databases/carbon_tracking.db')

PILOT_MONTHS = [
    ('2025-02',28),('2025-03',31),('2025-04',30),('2025-05',31),('2025-06',30),('2025-07',31),('2025-08',31),('2025-09',30),('2025-10',31)
]


def write_log(path: Path, lines):
    path.write_text("\n".join(lines)+"\n", encoding='utf-8')


def q(conn, sql, params=()):
    cur = conn.cursor(); cur.execute(sql, params); return cur.fetchall()


def gen_db_actual():
    if not DB_PATH.exists():
        write_log(LOG_DIR / 'db_actual_carbon_emissions.log', [
            'CARBON EMISSIONS LOG (DB ACTUAL)',
            '口徑說明：本檔案完全依據資料庫 visit_records 實際數據彙整。',
            '欄位中文說明：visits=訪視次數；total_km=行駛里程(公里)；total_kg_co2e=碳排(公斤二氧化碳當量)',
            'STATUS: database not found'
        ])
        return
    conn = sqlite3.connect(str(DB_PATH))
    res = q(conn, "SELECT MIN(visit_date), MAX(visit_date) FROM visit_records")
    min_date, max_date = res[0] if res else (None, None)
    by_worker = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1,2 ORDER BY 5 DESC")
    by_month = q(conn, "SELECT strftime('%Y-%m', visit_date), COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1 ORDER BY 1")
    by_transport = q(conn, "SELECT transport_type, COUNT(*), ROUND(SUM(distance),1), ROUND(SUM(COALESCE(carbon_emission,0)),1) FROM visit_records GROUP BY 1 ORDER BY 4 DESC")
    conn.close()
    tv = sum(r[2] for r in by_worker) if by_worker else 0
    tk = sum(r[3] for r in by_worker) if by_worker else 0
    tg = sum(r[4] for r in by_worker) if by_worker else 0
    lines = [
        'CARBON EMISSIONS LOG (DB ACTUAL)',
        '口徑說明：本檔案完全依據資料庫 visit_records 實際數據彙整。',
        '欄位中文說明：visits=訪視次數；total_km=行駛里程(公里)；total_kg_co2e=碳排(公斤二氧化碳當量)',
        f'PERIOD: {min_date} to {max_date}',
        f'TOTAL_VISITS: {int(tv)}',
        f'TOTAL_KM: {tk}',
        f'TOTAL_KG_CO2E: {tg}',
        '',
        'BY_WORKER (TOP 20):',
        'worker_id,worker_name,visits,total_km,total_kg_co2e',
    ]
    for row in by_worker[:20]:
        lines.append(','.join(str(x) for x in row))
    lines += ['', 'BY_MONTH:', 'year_month,visits,total_km,total_kg_co2e']
    for row in by_month:
        lines.append(','.join(str(x) for x in row))
    lines += ['', 'BY_TRANSPORT:', 'transport,visits,total_km,total_kg_co2e']
    for row in by_transport:
        lines.append(','.join(str(x) for x in row))
    write_log(LOG_DIR / 'db_actual_carbon_emissions.log', lines)


def gen_pilot_modeled():
    # 輕量版：每月 1200 筆模擬訪視，依 DB 分布抖動
    if not DB_PATH.exists():
        # 以預設分布建立少量樣本
        workers = [('SW%03d'%i, n) for i,n in [(1,'王小明'),(2,'李小華'),(3,'張小美'),(4,'吳宜靜'),(5,'林怡君')]]
        transport = [('機車',0.65,0.063),('汽車',0.30,0.2171),('大眾運輸',0.05,0.0573)]
    else:
        conn = sqlite3.connect(str(DB_PATH))
        w = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*) FROM visit_records GROUP BY 1,2 ORDER BY 3 DESC LIMIT 15")
        total = sum(r[2] for r in w) or 1
        workers = [ (r[0], r[1], r[2]/total) for r in w ] or [('SW001','王小明',0.2),('SW002','李小華',0.2),('SW003','張小美',0.2),('SW004','吳宜靜',0.2),('SW005','林怡君',0.2)]
        t = q(conn, "SELECT transport_type, COUNT(*), AVG(distance) FROM visit_records GROUP BY 1 ORDER BY 2 DESC")
        t_total = sum(r[1] for r in t) or 1
        # 係數查表
        coeff = {'機車':0.063,'汽車':0.2171,'大眾運輸':0.0573}
        transport = [(r[0], r[1]/t_total, coeff.get(r[0],0.1)) for r in t] or [('機車',0.65,0.063),('汽車',0.30,0.2171),('大眾運輸',0.05,0.0573)]
        conn.close()
    # 模擬
    by_worker = {}
    by_month = {}
    by_transport = {k:[0,0.0,0.0] for k,_,_ in transport}
    avg_dist = 12.0
    for ym, days in PILOT_MONTHS:
        monthly_visits = 1200 + random.randint(-150, 150)
        for _ in range(monthly_visits):
            if len(workers[0])==2:
                wid,wname = random.choice(workers)
            else:
                wid,wname,p = random.choices(workers, weights=[x[2] for x in workers])[0]
            t, tw, c = random.choices(transport, weights=[x[1] for x in transport])[0]
            dist = max(0.6, random.gauss(avg_dist, avg_dist*0.35))
            kg = dist * c
            # worker
            agg = by_worker.setdefault((wid,wname), [0,0.0,0.0])
            agg[0]+=1; agg[1]+=dist; agg[2]+=kg
            # month
            agg2 = by_month.setdefault(ym, [0,0.0,0.0])
            agg2[0]+=1; agg2[1]+=dist; agg2[2]+=kg
            # transport
            by_transport[t][0]+=1; by_transport[t][1]+=dist; by_transport[t][2]+=kg
    total_visits = sum(v[0] for v in by_worker.values())
    total_km = sum(v[1] for v in by_worker.values())
    total_kg = sum(v[2] for v in by_worker.values())
    lines = [
        'CARBON EMISSIONS LOG (PILOT PERIOD, MODELED)',
        '口徑說明：本檔案為試營運期 2025/02–10 之模型化數據，用於呈現變化特徵；非實際資料。',
        '欄位中文說明：visits=訪視次數；total_km=行駛里程(公里)；total_kg_co2e=碳排(公斤二氧化碳當量)',
        f'TOTAL_VISITS: {int(total_visits)}',
        f'TOTAL_KM: {total_km:.1f}',
        f'TOTAL_KG_CO2E: {total_kg:.1f}',
        '', 'BY_WORKER (TOP 15):','worker_id,worker_name,visits,total_km,total_kg_co2e'
    ]
    for (wid,wname), v in sorted(by_worker.items(), key=lambda x: -x[1][2])[:15]:
        lines.append(f"{wid},{wname},{v[0]},{v[1]:.1f},{v[2]:.1f}")
    lines += ['', 'BY_MONTH:','year_month,visits,total_km,total_kg_co2e']
    for ym, v in sorted(by_month.items()):
        lines.append(f"{ym},{v[0]},{v[1]:.1f},{v[2]:.1f}")
    lines += ['', 'BY_TRANSPORT:','transport,visits,total_km,total_kg_co2e']
    for t, v in by_transport.items():
        lines.append(f"{t},{v[0]},{v[1]:.1f},{v[2]:.1f}")
    write_log(LOG_DIR / 'pilot_modeled_carbon_emissions.log', lines)

if __name__ == '__main__':
    gen_db_actual()
    gen_pilot_modeled()
