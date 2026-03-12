#เพิ่มข้อมูลใหม่

import sqlite3  # import sqlite
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
c = conn.cursor()

try:
    data = [
        ('Songpon', 'Prathumma', 'Songpon.pr@kkumail.com'),
        ('Teerarin', 'Purisarn', 'Teerarin.p@kkumail.com'),
        ('wirasinee', 'tongkwan', 'wirasinee.tk@kkumail.com')
    ]
    
    c.executemany('INSERT INTO users (fname,lname,email) VALUES (?,?,?)', data)
    #executemany ใช้สำหรับรัน SQL หลายครั้ง
    
    conn.commit()
    c.close()

except sqlite3.Error as e:
    #เก็บรายละเอียด error ไว้ในตัวแปร e
    
    print('Failed to insert :', e)

finally:
    if conn:
        conn.close()