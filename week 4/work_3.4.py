while True:
    print('Mini shop\n เพิ่ม : A\n แสดง : B\n ออกจากระบบ : X\n -------------------------------')
    
    r = 0
    x = str(input('กรุณาเลือก : '))
    
    if x == 'A' :
        print('-------------------------------')
        c =[]
        
        A = str(input('กรุณากรอก ชื่อ นามสกุล :'))
        c.append(A)
        
        A = str(input('กรุณากรอก เบอร์โทร :'))
        c.append(A)
        
        A = str(input('กรุณากรอก Gmail :'))
        c.append(A)
        
        print('-------------------------------')
        
    if x == 'B' :
        print('-------------------------------')
        
        print('ชื่อ - นามสกุล :' , c[0])
        
        print('เบอร์โทร : ' , c[1])
        
        print('Gmail : ' , c[2])
        
        print('-------------------------------')
    
        A = str(input('กด X เพื่อกลับสู่หน้าหลัก :'))
        if A == 'X' :
            continue
        
    if x == 'X' :
        print('-------------------------------')
        A = str(input('ต้องการปิดโปรแกรมใช่หรือไม่ (yes or no): '))
        
        if A == 'yes' :
            break
        
        if A == 'no' :
            continue