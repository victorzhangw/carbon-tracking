import sqlite3, math
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
LOG_DIR = BASE / 'logs'
LOG_DIR.mkdir(exist_ok=True)
DB_PATH = Path('data/databases/carbon_tracking.db')

PILOT_START = '2025-02-01'
PILOT_END = '2025-10-31'


def write_log(path: Path, lines):
    path.write_text('\n'.join(lines)+'\n', encoding='utf-8')


def q(conn, sql, params=()):
    cur = conn.cursor(); cur.execute(sql, params); return cur.fetchall()


def gen_full_actual():
    if not DB_PATH.exists():
        return
    conn = sqlite3.connect(str(DB_PATH))
    res = q(conn, "SELECT MIN(visit_date), MAX(visit_date) FROM visit_records")
    min_date, max_date = res[0] if res else (None, None)
    by_worker = q(conn, "SELECT social_worker_id, social_worker_name, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1,2 ORDER BY 5 DESC")
    by_month = q(conn, "SELECT strftime('%Y-%m', visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 1")
    by_transport = q(conn, "SELECT transport_type, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 4 DESC")
    by_day = q(conn, "SELECT date(visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) FROM visit_records GROUP BY 1 ORDER BY 1 DESC LIMIT 60")
    long_trips = q(conn, "SELECT date(visit_date), social_worker_id, social_worker_name, transport_type, distance, COALESCE(carbon_emission,0) FROM visit_records WHERE distance > 50 ORDER BY distance DESC LIMIT 50")
    pd = q(conn, "SELECT social_worker_id, social_worker_name, date(visit_date), COUNT(*) FROM visit_records GROUP BY 1,2,3")
    # 高負載偵測
    from collections import defaultdict
    wc = defaultdict(list)
    for wid,wname,d,c in pd:
        wc[(wid,wname)].append(c)
    high_days=[]
    for (wid,wname),arr in wc.items():
        mean=sum(arr)/len(arr)
        var=sum((x-mean)**2 for x in arr)/len(arr)
        sd=math.sqrt(var)
        thr=mean+3*sd
        for ww, wn, d, c in pd:
            if ww==wid and wn==wname and c>thr and c>=10:
                high_days.append((d, wid, wname, c, round(mean,2), round(sd,2), round(thr,2)))
    seen=set(); filtered=[]
    for r in high_days:
        key=(r[0],r[1]);
        if key not in seen:
            seen.add(key); filtered.append(r)
    filtered.sort(key=lambda x:(-x[3], x[0]))
    filtered=filtered[:50]

    tv=sum(r[2] for r in by_worker) if by_worker else 0
    tk=sum(r[3] for r in by_worker) if by_worker else 0.0
    tg=sum(r[4] for r in by_worker) if by_worker else 0.0

    L=[]
    L.append('碳排放日誌（全期間，資料庫實際彙整）')
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
    L.append('最近60日彙總（依日）')
    L.append('日期,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    for r in by_day:
        L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    L.append('')
    L.append('異常偵測：單次距離>50公里（前50）')
    L.append('日期,工號,姓名,交通工具,距離(公里),碳排(公斤CO2e)')
    if long_trips:
        for r in long_trips:
            L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{float(r[4]):.1f},{float(r[5]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('異常偵測：單人單日訪視過高（> 平均+3σ，且至少10次；前50）')
    L.append('日期,工號,姓名,當日訪視數,個人日均值,日標準差,門檻值')
    if filtered:
        for r in filtered:
            L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]}')
    else:
        L.append('無資料')

    write_log(LOG_DIR / 'carbon_emissions.log', L)
    conn.close()


def gen_pilot_actual():
    # 依期間篩選（2025/02–10）的實際值（若無資料，輸出空口徑與無資料標註）
    if not DB_PATH.exists():
        return
    conn = sqlite3.connect(str(DB_PATH))
    by_worker = q(conn, (
        "SELECT social_worker_id, social_worker_name, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? GROUP BY 1,2 ORDER BY 5 DESC"), (PILOT_START, PILOT_END))
    by_month = q(conn, (
        "SELECT strftime('%Y-%m', visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? GROUP BY 1 ORDER BY 1"), (PILOT_START, PILOT_END))
    by_transport = q(conn, (
        "SELECT transport_type, COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? GROUP BY 1 ORDER BY 4 DESC"), (PILOT_START, PILOT_END))
    by_day = q(conn, (
        "SELECT date(visit_date), COUNT(*), SUM(distance), SUM(COALESCE(carbon_emission,0)) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? GROUP BY 1 ORDER BY 1"), (PILOT_START, PILOT_END))
    long_trips = q(conn, (
        "SELECT date(visit_date), social_worker_id, social_worker_name, transport_type, distance, COALESCE(carbon_emission,0) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? AND distance > 50 ORDER BY distance DESC LIMIT 50"), (PILOT_START, PILOT_END))
    pd = q(conn, (
        "SELECT social_worker_id, social_worker_name, date(visit_date), COUNT(*) "
        "FROM visit_records WHERE visit_date BETWEEN ? AND ? GROUP BY 1,2,3"), (PILOT_START, PILOT_END))
    from collections import defaultdict
    wc = defaultdict(list)
    for wid,wname,d,c in pd:
        wc[(wid,wname)].append(c)
    filtered=[]
    for (wid,wname),arr in wc.items():
        mean=sum(arr)/len(arr)
        var=sum((x-mean)**2 for x in arr)/len(arr)
        sd=math.sqrt(var)
        thr=mean+3*sd
        for ww, wn, d, c in pd:
            if ww==wid and wn==wname and c>thr and c>=10:
                filtered.append((d, wid, wname, c, round(mean,2), round(sd,2), round(thr,2)))
    filtered.sort(key=lambda x:(-x[3], x[0]))

    tv=sum(r[2] for r in by_worker) if by_worker else 0
    tk=sum(r[3] for r in by_worker) if by_worker else 0.0
    tg=sum(r[4] for r in by_worker) if by_worker else 0.0

    L=[]
    L.append('碳排放日誌（試營運期間，資料庫實際彙整）')
    L.append('資料來源：data/databases/carbon_tracking.db / 表：visit_records；期間：2025/02/01–2025/10/31')
    L.append('欄位中文說明：訪視次數=visits；行駛里程(公里)=total_km；碳排(公斤CO2e)=total_kg_co2e')
    L.append(f'總訪視次數：{int(tv)}')
    L.append(f'總里程(公里)：{tk:.1f}')
    L.append(f'總碳排(公斤CO2e)：{tg:.1f}')
    L.append('')
    L.append('依社工彙總（前20名）')
    L.append('工號,姓名,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    if by_worker:
        for r in by_worker[:20]:
            L.append(f'{r[0]},{r[1]},{int(r[2])},{float(r[3]):.1f},{float(r[4]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('依月份彙總')
    L.append('年月,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    if by_month:
        for r in by_month:
            L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('依交通工具彙總')
    L.append('交通工具,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    if by_transport:
        for r in by_transport:
            L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('依日彙總（by_day）')
    L.append('日期,訪視次數,行駛里程(公里),碳排(公斤CO2e)')
    if by_day:
        for r in by_day:
            L.append(f'{r[0]},{int(r[1])},{float(r[2]):.1f},{float(r[3]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('異常偵測：單次距離>50公里（前50）')
    L.append('日期,工號,姓名,交通工具,距離(公里),碳排(公斤CO2e)')
    if long_trips:
        for r in long_trips:
            L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{float(r[4]):.1f},{float(r[5]):.1f}')
    else:
        L.append('無資料')
    L.append('')
    L.append('異常偵測：單人單日訪視過高（> 平均+3σ，且至少10次）')
    L.append('日期,工號,姓名,當日訪視數,個人日均值,日標準差,門檻值')
    if filtered:
        for r in filtered[:50]:
            L.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{r[4]},{r[5]},{r[6]}')
    else:
        L.append('無資料')

    write_log(LOG_DIR / 'pilot_carbon_emissions.log', L)
    conn.close()

if __name__ == '__main__':
    gen_full_actual()
    gen_pilot_actual()
