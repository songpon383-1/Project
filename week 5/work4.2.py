#เพิ่มคำศัพท์

i = 0
m = ''
all = []

def Menu():
    global m
    print('1) เพิ่มคำศัพท์\n2) แสดงคำศัพท์\n3) ลบคำศัพท์\n4) ออกจากโปรแกรม')
    print('{0:-<40}'.format(''))
    m = input('Input Choice : ')

def word():
    global i , all
    a  = input('เพิ่มคำศัพท์ : ')
    b = input('ชนิดคำศัพท์ (n , v , adj , adv) : ')
    c = input('ความหมาย : ')
    all.append([a , b , c])
    i += 1
    print("เพิ่มคำศัพท์เรียบร้อย")
    print('{0:-<40}'.format(''))


def show():
    print('คำศัพท์ทั้งหมด', i , 'คำ')
    print('{0:-<60}'.format(''))
    print(f'{"คำศัพท์":<25}\t{"ประเภท":<10}\t{"ความหมาย"}')
    for verb in all:
        print(f'{verb[0]:<25}\t{verb[1]:<10}\t{verb[2]}')
    print('{0:-<60}'.format(''))

def delete():
    global i , all
    d = input('พิมพ์คำศัพท์ที่ต้องการลบ : ')
    f = False
    for verb in all:
        if verb[0] == d:
            e = input(f'ต้องการลบ "{d}" ใช่หรือไม่ (yes or no) : ')
            if e.lower() == 'yes':
                all.remove(verb)
                i -= 1
                print(f'ลบ "{d}" เรียบร้อยแล้ว')
            f = True
            break
    if not f:
        print('ไม่พบคำศัพท์ที่ต้องการลบ')

while True:
    Menu()
    if m == '1':
        word()
    elif m == '2':
        show()
        print('Exit [x]')
        h = input('Enter your choice :')
        print('{0:-<40}'.format(''))
        if h == 'x':
            continue
    elif m == '3':
        delete()
    elif m == '4':
        break
    else:
        print("กรุณาเลือก 1-4 เท่านั้น")
        print('{0:-<30}'.format(''))