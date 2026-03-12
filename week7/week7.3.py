#เพิ่มข้อมูลใหม่

import sqlite3                                               # import sqlite

def insertTousers (fname,lname,email):
    try :
        conn = sqlite3.connect(r'D:\Code_Python\Code\week7\SQ.db')   
        c = conn.cursor()                                            

        sql = ''' INSERT INTO users (fname,lname,email) VALUES (?,?,?)'''
        data = (fname,lname,email)
        c.execute(sql,data)
        conn.commit()  
        c.close()                                              
    
    except sqlite3.Error as e:
        print('Failed to insert : ',e)
    finally:         
        if conn :
         conn.close()
insertTousers('Guido','Rossum','Python@gmail.com')
insertTousers('Dennis','Ritchie','abc')
