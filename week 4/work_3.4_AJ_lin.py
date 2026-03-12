while True:
    b = input('Mini shop\n เพิ่ม : A\n แสดง : B\n ออกจากระบบ : X\n -------------------------------\n : ')
    b = b.lower()
    if b == 'a' :
        c = input('รหัส ชื่อ จังหวัด')
        a.append(c)
    elif b == 's' :
        print('{0:-<30}'.format(''))
        print('{0:*<6}{1:-<10}{2:10}'.format('รหัส' , 'ชื่อ' , 'จังหวัด'))
        print('{0:~<30}'.format(''))
        for d in a :
            e = d.split(':')
            print('{0[0]:<6} {0[1]10}({0[2]:<10})'.format(e))
            continue
    elif b == 'x':
        c = input('ต้องการปิดโปรแกรมใช่หรือไม่ y/n :')
        if c == 'y':
            break
        else :
            continue