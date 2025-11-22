import sqlite3

conn = sqlite3.connect('data/databases/emotion_analysis.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM score_records WHERE user_id="demo_user"')
count = cursor.fetchone()[0]
print(f'✅ 資料庫中有 {count} 筆 demo_user 的記錄')

# 查看分頁情況
for page_size in [10, 20, 50, 100]:
    total_pages = (count + page_size - 1) // page_size
    print(f'   {page_size} 筆/頁 = {total_pages} 頁')

conn.close()
