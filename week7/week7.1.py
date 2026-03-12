# สร้างตารางใน SQlite

import sqlite3                                  # import sqlite เชื่อมต่อและจัดการฐานข้อมูล SQLite

conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   # เชื่อมต่อ database SQLite
c = conn.cursor()                                            # create a cursor object

#สร้างตารางใหม่ ถ้าตารางชื่อ users มีอยู่แล้ว จะไม่สร้างใหม่
c.execute('''CREATE TABLE IF NOT EXISTS users  
           (id INTEGER PRIMARY KEY AUTOINCREMENT,
           fname VARCHAR(30) NOT NULL,
           lname VARCHAR(30) NOT NULL,
           email VARCHAR(100) NOT NULL)''')

 #id  ชื่อคอลัมน์

#INTEGER  เก็บค่าเป็นตัวเลขจำนวนเต็ม

#PRIMARY KEY  เป็น คีย์หลัก ห้ามซ้ำ, ห้ามว่าง

#AUTOINCREMENT  เมื่อมีการเพิ่มข้อมูลใหม่ ค่า id จะเพิ่มขึ้นเองอัตโนมัติ

conn.commit()                                                # save (commit) the changes
conn.close()                                                 # close the connection when done