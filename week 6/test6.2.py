#1
try:
    print('hello' + 'hi')
except: #จะทำงานถ้าเกิด ข้อผิดพลาด
    print('Error!!!')

#ตัวอย่างที่ Error    
try:
    print('hello' + 5)
except:
    print('Error!!!')



#2
try:
    print('hello' + 'hi')
except:
    print('Error!!!')
else:
    print('No Error >')
finally:
    print('Finich')
    


#3
try:
    print('hello' + 5)
except:
    print('Error!!!')
else:
    print('No Error >')
finally:
    print('Finich')