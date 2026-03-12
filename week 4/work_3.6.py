c = []  # เก็บตะกร้าเป็น list ของ index สินค้าที่หยิบ

#กำหนดให้ product มีค่าทั้งหมด 5 ตัว
product = [ 
    ['มาม่า' , 15], #1
    ['โค้ก' , 10], #2
    ['ยาสีฟัน' , 20], #3
    ['ผงซักผ้า' , 25], #4
    ['ไก่' , 45] #5
]

while True: #วาย ทรู
    
    #กำหนดให้ data มีค่าทั้งหมด 5 ตัว
    data = [
        ['แสดงรายการสินค้า' , '[1]'], #1
        ['หยิบสินค้าเข้าตระกร้า' , '[2]'], #2
        ['แสดงรายการจำนวนและราคาของสินค้าที่หยิบ' , '[3]'], #3
        ['หยิบสินค้าออกจากตะกร้า' , '[4]'], #4
        ['ปิดโปรแกรม' , '[x]'] #5
    ]
    
    for i in range(len(data)):  
        # range(เร้น) สร้างตัวเลขของ len(เลน)(data) ขึ้นมา     
        # len(เลน) คืนค่าความยาวลิสต์ หรือ สตริง 
        # วน i ใน reang(เร้น)(len(เลน)(data(ดาต้า)))
        
        print(f'{data[i][0]:<35}\t{data[i][1]:<5}') 
        # ปริ้น ดาต้า ในตำแหน่งที่ i และตำแหน่งที่ 0 ไปทางซ้าย 35 
    x = input('กรุณาเลือกทำรายการ : ')

    # แสดงรายการสินค้า
    if x == '1':
        while True:
            for i in range(len(product)):
                p = product[i]
                print(f'{p[0]:<25}\t฿{p[1]:<8}\t[{i+1}]')
            print('[x] ออกจากฟังก์ชัน')
            A = input('กรุณาเลือกทำรายการ : ')
            if A == 'x':
                break

    # หยิบสินค้าเข้าตระกร้า
    elif x == '2':
        while True:
            for i in range(len(product)):
                p = product[i]
                print(f'{p[0]:<25}\t\t[{i+1}]')
            print('[x] ออกจากฟังก์ชัน')
            A = input('กรุณาเลือกหยิบสินค้าหมายเลข : ')
            if A == 'x':
                break
            if A.isdigit() and 1 <= int(A) <= len(product):
                c.append(int(A)-1)    
            else:
                print('กรุณาเลือกสินค้าที่กำหนด')

    # แสดงรายการสินค้าในตระกร้า
    elif x == '3':
        print('---------------------------------------------')
        print(f'{"สินค้า":<25} {"จำนวน":<10} {"ราคารวม"}')
        total_price = 0
        total_items = 0
        count = [0] * len(product)
        for i in c:
            count[i] += 1
        for i in range(len(product)):
            if count[i] > 0:
                name = product[i][0]
                price = product[i][1]
                pieces = count[i]
                total = pieces * price
                total_price += total
                total_items += pieces
                print(f'{name:<25} {pieces:<10} {total}')
        print('---------------------------------------------')
        print(f'รวมทั้งหมด {total_items} ชิ้น\t\tรวมราคา ฿{total_price}')
        print('---------------------------------------------')
        A = input('Back to menu [x] : ')
        if A == 'x':
            continue

    # ลบสินค้าออกจากตะกร้า
    elif x == '4':
        while True:
            if not c:
                print("ไม่มีสินค้าในตะกร้า")
                break
            count = [0] * len(product)
            for i in c:
                count[i] += 1
            for i in range(len(product)):
                if count[i] > 0:
                    print(f'[{i+1}] {product[i][0]} จำนวน {count[i]}')
            print('[x] ออกจากฟังก์ชัน')
            A = input('พิมพ์หมายเลขสินค้าที่ต้องการลบ 1 ชิ้น : ')
            if A == 'x':
                break
            if A.isdigit():
                index = int(A) - 1
                if index in c:
                    c.remove(index)
                    print(f'ลบ {product[index][0]} ออก 1 ชิ้น')
                else:
                    print('ไม่มีสินค้านี้ในตะกร้า')
            else:
                print('กรุณาใส่เลขให้ถูกต้อง')
                
    elif x == 'x':
        A = input('ต้องการปิดโปรแกรมใช่หรอไม่ [yes or no] :')
        if A == 'yes':
            print('ขอบคุณที่ใช้บริการ')
            break
        if A == 'no':
            continue
        