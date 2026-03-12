c = []  #ใช้เป็นตะกร้า

while True: #วาย ทรู
    
    data = [ #กำหนดให้ data มีค่าทั้งหมด 5 ตัว
        ['Nike' , '[1]'],#1
        ['Adidas' , '[2]'],#2
        ['Converse' , '[3]'],#3
        ['Show basket' , '[4]'],#4
        ['Exit' , '[x]']#5
    ]
    for x in data: #วน x ใน data
        
        print(f'{x[0]:<10}\t{x[1]:<5}')
        #ปลิ้น x ตำแหน่งที่ 0 เว้นไปทางซ้าย 10 ปลิ้น x ตำแหน่งที่ 1 เว้นไปทางซ้าย 5
        
    x = input('Enter : ') # x = อินพุทคำว่าเอ็นเตอร์
    
    # Nike
    if x == '1':  #อิฟ x == 1 
        
        while True: 
            #คำสั่ง  วาย ทรู ลูป
            
            #กำหนดให้ nike มีค่าทั้งหมด 4 ตัว
            nike = [ 
                ['Nike Dunk Low Retro SE' , '฿4,700' , '[1]'], #1
                ['Nike Air Max 90 Premium' , '฿5,400' , '[2]'], #2
                ['Nike Terra Manta' , '฿3,200' , '[3]'], #3
                ['Back to menu' , '' , '[x]'] #4
            ]
            
            for x in nike: #วน x ในnike
                
                print(f'{x[0]:<25}\t{x[1]:<8}\t{x[2]}') 
                #ปลิ้น x ตำแหน่งที่ 0 เว้นไปทางซ้าย 25 ปลิ้น x ตำแหน่งที่ 1 เว้นไปทางซ้าย 8 และ ปลิ้น x ตำแหน่งที่ 2
                
            A = input('The product you choose : ') 
            #กำหนด A = อินพุท สินค้าที่ผู้ใช้เลือก
            
            if A == 'x': #อิฟ a == x
                break
            
            if A.isdigit() and 1 <= int(A) <= 3: 
                #อิฟ เอ ไอ เอส ดิจิท แอน 1 น้อยกว่าเท่ากับ อิ้นเอ น้อยกว่าเท่ากับ 3
                #ไอ เอส ดิจิท คือการตรวจสอบว่าข้อมูลที่รับมาเป็นตัวเลขไหม เช่น 1 2 3 หากไม่ใช่จะ เออเร่อ 
                #1 <= int(A) <= 3 เป็นการตรวจสอบว่า int(A) หรือ ค่า A ที่รับมาอยู่ระหว่างเลข ที่กำหนดมาหรือไม่
                #เพราะ nike บรรทัด 18 nike มีให้เลือกสินค้าเพียง เลข 1 2 3 หากไม่ใช่เลขนี้จะขึ้น เออเร่อ
                
                c.append((0, int(A) - 1)) 
                #ซี แอฟเพ่น 0 int(A)-1 คือการเก็บข้อมูลของ nike ตำแหน่งที่ 0 และ int(A)-1 ไว้ใน c=[]
                #ที่เอาเอมาลบ 1 เพราะต้องการหา index (อินเด็ก) ของ nike แต่คอมพิวเตอร์เริ่มนับตั้งแต่เลข 0
    # Adidas
    if x == '2': #อิฟ x == 2 
        
        while True: #ใช้คำสั่ง วาย ทรู
            
            #กำหนดให้ adidas มีค่าทั้งหมด 4 ตัว
            adidas = [
                ['SAMBA OG' , '฿3,800' , '[1]'], #1
                ['Adizero EVO SL' , '฿5,800' , '[2]'], #2
                ['CLIMACOOL' , '฿5,700' , '[3]'], #3
                ['Back to menu' , '' , '[x]'] #4
            ]
            
            for x in adidas: #วน x ใน adidas
                
                print(f'{x[0]:<25}\t{x[1]:<8}\t{x[2]}') 
                #ปลิ้น x ตำแหน่งที่ 0 เว้นไปทางซ้าย 25 ปลิ้น x ตำแหน่งที่ 1 เว้นไปทางซ้าย 8 และ ปลิ้น x ตำแหน่งที่ 2
                
            A = input('The product you choose : ') 
            #กำหนด A = อินพุท สินค้าที่ผู้ใช้เลือก
            
            if A == 'x': #อิฟ a == x
                break
            
            if A.isdigit() and 1 <= int(A) <= 3:
                #อิฟ เอ ไอ เอส ดิจิท แอน 1 น้อยกว่าเท่ากับ อิ้นเอ น้อยกว่าเท่ากับ 3
                #ไอ เอส ดิจิท คือการตรวจสอบว่าข้อมูลที่รับมาเป็นตัวเลขไหม เช่น 1 2 3 หากไม่ใช่จะ เออเร่อ 
                #1 <= int(A) <= 3 เป็นการตรวจสอบว่า int(A) หรือ ค่า A ที่รับมาอยู่ระหว่างเลข ที่กำหนดมาหรือไม่
                #เพราะ nike บรรทัด 41 adidas มีให้เลือกสินค้าเพียง เลข 1 2 3 หากไม่ใช่เลขนี้จะขึ้น เออเร่อ
                
                c.append((1, int(A) - 1)) #ซี แอฟเพ่น 0 int(A)-1 คือการเก็บข้อมูลของ adidas ตำแหน่งที่ 0 และ int(A)-1 ไว้ใน c=[]
                #ที่เอาเอมาลบ 1 เพราะต้องการหา index (อินเด็ก) ของ adidas แต่คอมพิวเตอร์เริ่มนับตั้งแต่เลข 0
    
    # Converse
    if x == '3': 
        #อิฟ x == 3 
        
        while True: 
            #ใช้คำสั่ง วาย ทรู
            
            #กำหนดให้ converse มีค่าทั้งหมด 4 ตัว
            converse = [
                ['Chuck 70 Pride' , '฿3,790' , '[1]'], #1
                ['Chuck 70 Fire' , '฿3,400' , '[2]'], #2
                ['Chuck 70' , '฿3,290' , '[3]'], #3
                ['Back to menu' , '' , '[x]'] #4
            ]
            
            for x in converse: 
                #วน x ใน converse
                
                print(f'{x[0]:<25}\t{x[1]:<8}\t{x[2]}') 
                #ปลิ้น x ตำแหน่งที่ 0 เว้นไปทางซ้าย 25 ปลิ้น x ตำแหน่งที่ 1 เว้นไปทางซ้าย 8 และ ปลิ้น x ตำแหน่งที่ 2
                
            A = input('The product you choose : ') 
            #กำหนด A = อินพุท สินค้าที่ผู้ใช้เลือก
            
            if A == 'x': #อิฟ a == x
                break
            
            if A.isdigit() and 1 <= int(A) <= 3: 
                #อิฟ เอ ไอ เอส ดิจิท แอน 1 น้อยกว่าเท่ากับ อิ้นเอ น้อยกว่าเท่ากับ 3
                #ไอ เอส ดิจิท คือการตรวจสอบว่าข้อมูลที่รับมาเป็นตัวเลขไหม เช่น 1 2 3 หากไม่ใช่จะ เออเร่อ 
                #1 <= int(A) <= 3 เป็นการตรวจสอบว่า int(A) หรือ ค่า A ที่รับมาอยู่ระหว่างเลข ที่กำหนดมาหรือไม่
                #เพราะ converse บรรทัด 62 converse มีให้เลือกสินค้าเพียง เลข 1 2 3 หากไม่ใช่เลขนี้จะขึ้น เออเร่อ
                
                c.append((2, int(A) - 1)) 
                #ซี แอฟเพ่น 0 int(A)-1 คือการเก็บข้อมูลของ converse ตำแหน่งที่ 0 และ int(A)-1 ไว้ใน c=[]
                #ที่เอาเอมาลบ 1 เพราะต้องการหา index (อินเด็ก) ของ converse แต่คอมพิวเตอร์เริ่มนับตั้งแต่เลข 0
    
    # Show basket
    if x == '4': 
        #อิฟ x == 4 
        
     Nike_discount = ['0', '0', '0'] 
     #ให้ nike ดิสเค้า มีค่า 3 ตัว 
     
     Adidas_discount = ['1140', '0', '0'] 
     #ให้ Adidas ดิสเค้า มีค่า 3 ตัว
     
     Converse_discount = ['379', '0', '0'] 
     #ให้ Converse ดิสเค้า มีค่า 3 ตัว
      
     All_discount = [Nike_discount, Adidas_discount, Converse_discount] 
     #นำตัวแปลทั้ง 3 ตัวมาเก็บไว้ใน All discount(ดิสเค้า)

     Nike_price = ['4700', '5400', '3200'] 
     #ให้ nike ไพร้ซ์ มีค่า 3 ตัว 
     
     Adidas_price = ['3800', '5800', '5700'] 
     #ให้ Adidas ไพร้ซ์ มีค่า 3 ตัว
     
     Converse_price = ['3790', '3400', '3290'] 
     #ให้ Converse ไพร้ซ์ มีค่า 3 ตัว
     
     Price = [Nike_price, Adidas_price, Converse_price]
     #นำตัวแปลทั้ง 3 ตัวมาเก็บไว้ใน price(ไพร้ซ์) 

     Nike = ['Nike Dunk Low Retro SE', 'Nike Air Max 90 Premium', 'Nike Terra Manta'] 
     #ให้ nike มีค่า 3 ตัว คือ ชื่อยี่ห้อรองเท้าของแบรน
     
     Adidas = ['SAMBA OG', 'Adizero EVO SL', 'CLIMACOOL'] 
     #ให้ Adidas มีค่า 3 ตัว คือ ชื่อยี่ห้อรองเท้าของแบรน
     
     Converse = ['Chuck 70 Pride', 'Chuck 70 Fire', 'Chuck 70'] 
     #ให้ Converse มีค่า 3 ตัว คือ ชื่อยี่ห้อรองเท้าของแบรน
     
     All = [Nike, Adidas, Converse]
     #นำตัวแปลทั้ง 3 ตัวมาเก็บไว้ใน all(ออ)
    
     total_price = 0 
     #total_price(โทเทิ่ว ไพร้) = 0 
     
     total_discount = 0 
     #total_discount(โทเทิ่ว ดิสเค้า) = 0 

     print('---------------------------------------------')
     
     print(f'{"Product":<25} {"Discount":<10} {"Price"}') 
     #f คือการที่จะทำให้เพิ่มเลขที่เป็น loop ได้
     #Product(โปรดัค) :<25 ไปทางซ้าย 25 Discount(ดิสเค้า) :<10 ไปทางซ้าย 10 Price(ไพร้)
     
     for brand, product in c:    
         #วน brand(แบรน) product(โปรดัค) ใน c ใช้ตัวไหนก็ได้แต่ในที่นี้ใช้ brand and product โดยสองตัวนี้จะเป็นค่าที่เราเก็บไว้ใน c = []
         
         price = int(Price[brand][product]) 
         #ตัวแปร price(ไพร้) คือค่าของ (Price(ไพร้)[brand(แบรน)][product(โปรดัค)]) ที่ถูกทำให้เป็น int(อิ้น)
         #int คือการเปลี่ยนจากค่าที่คำนวนไม่ได้ให้คำนวนได้
         
         discount = int(All_discount[brand][product])
         #ตัวแปร discount(ดิสเค้า) คือค่าของ (All(ออ)_discount(ไพร้)[brand(แบรน)][product(โปรดัค)]) ที่ถูกทำให้เป็น int(อิ้น)
         #int คือการเปลี่ยนจากค่าที่คำนวนไม่ได้ให้คำนวนได้
         
         total_price += price 
         #total_price(โทเทิ่ว ไพร้) += price(ไพร้)
         
         total_discount += discount 
         #total_discount(โทเทิ่ว ดิสเค้า) += discount(ดิสเค้า)
         
         print(f'{All[brand][product]:<25} {All_discount[brand][product]:<10} {Price[brand][product]}')
        # {All(ออ)[brand(แบรน)][product(โปรดัค)]:<25} ไปทางซ้าย 25
        # {All(ออ)_discount(ดิสเค้า)[brand(แบรน)][product(โปรดัค)]:<10} ไปทางซ้าย 10
        # Price(ไพร้)[brand(แบรน)][product(โปรดัค)]
        
     net_price = total_price - total_discount 
     #net(เน็ต)_price(ไพร้) = total(โทเทิ้ว)_price(ไพร้) - total(โทเทิ้ว)_discount(ดิสเค้า)
     
     print('---------------------------------------------')
     print(f'Total Price               {total_discount:<10} {net_price}') 
     #total(โทเทิ้ว)_discount(ดิสเค้า):<10 ไปทางซ้าย 10  net(เน็ต)_price(ไพร้)
     print('---------------------------------------------')

     A = input('Back to menu [x] : ')
    if A == 'x':
        break