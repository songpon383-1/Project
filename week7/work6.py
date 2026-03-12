#แบบฝึกหัดที่ 6 

import sqlite3
    
conn = sqlite3.connect(r'D:\Code_Python\Code\week7\student.db')
c = conn.cursor()
    
c.execute('''CREATE TABLE IF NOT EXISTS users
        (number INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(30) NOT NULL,
        email VARCHAR(30) NOT NULL,
        gender VARCHAR(30) NOT NULL,
        year VARCHAR(30) NOT NULL,
        level VARCHAR(30) NOT NULL)''')
    
conn.commit()
conn.close() 


while True:    
    menu = [
        ('เพิ่มนักเรียน กด [a]'),
        ('แสดงข้อมูลนักเรียน กด [s]'),
        ('แก้ไขข้อมูลนักเรียน กด [e]'),
        ('ลบข้อมูลนักเรียน กด [d]'),
        ('ออกจากระบบ กด [x]')
    ]
    for m in menu:
        print(m)
        print('{0:-<40}'.format(''))
    x = input('Enter >>> ')
    
        
    #เพิ่มนักเรียน
    if x == 'a':
        name = input('กรอก ชื่อ - นามสกุล >>> ')
        email = input('กรอก email >>> ')
        gender = input('กรอก เพศ >>> ')
        year = input('กรอก อายุ >>> ')
        level = input('กรอก ชั้นปี >>> ')
            
        conn = sqlite3.connect(r'D:\Code_Python\Code\week7\student.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users (name , email , gender , year , level) VALUES (?,?,?,?,?)''',
                (name, email, gender, year, level))
        conn.commit()
        conn.close()
        print('{0:-<40}'.format(''))
        print('เพิ่มเรียบร้อยแล้ว ^o^')
            
            
    #แสดงข้อมูลนักเรียน   
    if x == 's':
        conn = sqlite3.connect(r'D:\Code_Python\Code\week7\student.db') 
        c = conn.cursor()
        c.execute('''SELECT * FROM users''')
        result = c.fetchall()
        for r in result:
            print(r)
            print('{0:-<40}'.format(''))
        conn.close()
                
                
    #แก้ไขข้อมูลนักเรียน        
    if x == 'e':
        print('กรอกข้อมูลที่แก้ไขของนักเรียน ^o^')
        print('{0:-<40}'.format(''))
        name = input('กรอก ชื่อ - นามสกุล >>> ')
        email = input('กรอก email >>> ')
        gender = input('กรอก เพศ >>> ')
        year = input('กรอก อายุ >>> ')
        level = input('กรอก ชั้นปี >>> ')
        num = int(input('กรอกแถวที่ต้องการแก้ไข >>> '))
        print('{0:-<40}'.format(''))
            
        conn = sqlite3.connect(r'D:\Code_Python\Code\week7\student.db')
        c = conn.cursor()
            
        try:
            c.execute('''UPDATE users SET name = ?, email = ?, gender = ?, year = ?, level = ? WHERE number = ?''',
                      (name, email, gender, year, level, num))
            conn.commit()
            c.close()
                
        except sqlite3.Error as e:
            print(e)
                
        finally:
            if conn:
                conn.close()
                    

#ลบข้อมูลนักเรียน                    
    if x == 'd':
        conn = sqlite3.connect(r'D:\Code_Python\Code\week7\student.db')
        c = conn.cursor()
            
        try: 
            num = int(input('กรอกแถวที่ต้องการลบ >>>'))
            c.execute('DELETE FROM users WHERE number = ?', (num,))
            print('{0:-<40}'.format(''))
            conn.commit()
            c.close()
                
        finally:
            if conn:
                conn.close()
                    
    if x == 'x':
        print('ขอบคุณที่ทำรายการ ^o^')
        break
