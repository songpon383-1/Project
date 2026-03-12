#show ข้อมูลทั้งหมด

import sqlite3                                               # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()
c.execute('''SELECT * FROM users''')
result = c.fetchall() #ดึงข้อมูลออกมาแสดง
for x in result:
    print(x)