#แก้ไขเฉพาะแถวที่ต้องการ

import sqlite3  # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

try:
    data = [
        ('ABC', 'XYZ', 'ABC@gmail.com','3') #3 คือ แถวที่ต้องการแก้ไข
    ]
    c.executemany('''UPDATE users SET fname =?,lname =?,email =? WHERE id =?''', data)
    conn.commit()
    c.close()

except sqlite3.Error as e:
    print(e)

finally:
    if conn:
        conn.close()