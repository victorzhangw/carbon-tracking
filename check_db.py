import sqlite3

conn = sqlite3.connect('carbon_tracking.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("資料庫中的表:", tables)
conn.close()
