#show ข้อมูลลำดับจากเลขมากไปน้อย

import sqlite3  # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

try:    
    c.execute('SELECT * FROM users ORDER BY id DESC')
    conn.commit()
    result = c.fetchall()
    for x in result:
        print(x)
    c.close()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()