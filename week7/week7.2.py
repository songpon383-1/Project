#เพิ่มข้อมูลใหม่

import sqlite3                                               # import sqlite

conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')

c = conn.cursor()
c.execute('''INSERT INTO users (id,fname,lname,email) VALUES (NULL,"Songpon","Prathumma","Songpon2549@gmail.com")''')   
c.execute('''INSERT INTO users VALUES (NULL,'Teerarin','Purisarn','Teerarin.p@kkumail.com')''')
#execute ใช้รันคำสั่ง SQL

conn.commit()
conn.close()