#ลบออกจาก users ทั้งหมด

import sqlite3  # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

try:    
    c.execute('DELETE FROM users ')    
    conn.commit()
    c.close()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()