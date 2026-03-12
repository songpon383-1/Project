#เปรียบเทียบราคาแบบจ่ายเพิ่ม กับ เหมาจ่าย

num = 0
print('\tเลือกเมนูเพื่อทำรายการ')
print('{0:-<30}'.format(''))
print('\tกด 1 เพื่อจ่ายเพิ่ม')
print('\tกด 2 เพื่อเหมาจ่าย')
print('{0:-<30}'.format(''))
x = input('Enter number : ')
if x == '1':
    print('{0:-<30}'.format(''))
    y = int(input('กรุณากรอกระยะทาง : '))
    if y < 25:
        num = num + 25
    elif y >= 25:
        num = num + 55 + 25
if x == '2':
    print('{0:-<30}'.format(''))
    y = int(input('กรุณากรอกระยะทาง : '))
    if y < 25:
        num = num + 25
    elif y >= 25:
        num = num + 55
print('{0:-<30}'.format(''))
print('ค่าใช้จ่าย รวมทั้งหมด' , num , 'บาท')
