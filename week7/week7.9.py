#show ข้อมูลตัวที่ต้องการ

import sqlite3                                               # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

name = ('wirasinee',) #name เป็นตัวแปร tuple
c.execute('SELECT * FROM users WHERE fname = ?',name)

result = c.fetchall() #ดึงข้อมูลออกมาแสดง
for x in result:
    print(x)