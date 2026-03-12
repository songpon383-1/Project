#show ข้อมูลเฉพาะที่ต้องการ

import sqlite3  # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

try:    
    c.execute('SELECT * FROM users LIMIT 5 OFFSET 1')    
    result = c.fetchall()
    for x in result:
        print(x)
    c.close()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()