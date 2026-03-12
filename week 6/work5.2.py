class Shop:
    def __init__(self , name):
        self.name = name
        self.products = [
            {"name": "ไส้กรอกชีส", "price": 49},
            {"name": "ขนมปังโอวัลติน", "price": 20},
            {"name": "นมซังซัง", "price": 10},
            {"name": "น้ำสิงห์", "price": 14},
            {"name": "น้ำแข็ง", "price": 8},
        ]

    def show_products(self):
        while True:
            if not self.products:
                print("ไม่มีสินค้าในร้าน ^o^")
                print('{0:-<20}'.format(''))
                x = input("Exit [x] : ")
                if x == 'x':
                    break
                elif x != 'x':
                    continue
            else:
                print('{0:-<20}'.format(''))
                print(f"\nรายการสินค้าของร้าน {self.name}")
                for i , p in enumerate(self.products , start=1):
                    print('{0:-<30}'.format(''))
                    print(f"{i}. {p['name']} ---> ราคา {p['price']} บาท")
                    print('{0:-<30}'.format(''))
                x = input('Exit [x] : ')
                if x == 'x':
                    break
                elif x != 'x':
                    continue

    def add_product(self , name , price):
        self.products.append({
            "name" : name,
            "price" : price,
        })
        print(f"เพิ่มสินค้า {name} เรียบร้อย ^o^ ")
        print('{0:-<20}'.format(''))

    def remove_product(self , name) :              
        for p in self.products :
            if p["name"] == name :
                self.products.remove(p)
                print(f"ลบสินค้า {name} สำเร็จ")
                print('{0:-<20}'.format(''))
                return
        print(f"ไม่พบสินค้า {name}")

shop = Shop("ร้านค้าNudeeสีชมพู ^o^ ")

while True:
    print("\t ^o^ เมนู ^o^")
    print("[1] แสดงรายการสินค้า")
    print("[2] เพิ่มรายการสินค้า")
    print("[3] ลบสินค้า")
    print("[x] ออกจากระบบ")
    print('{0:-<20}'.format(''))
    choice = input("\nเลือกเมนู ^o^ : ")

    if choice == "1":
        shop.show_products()
        
    elif choice == "2":
        name = input("ชื่อสินค้า : ")
        price = float(input("ราคาสินค้า : "))
        shop.add_product(name , price)
        
    elif choice == "3":
        name = input("ชื่อสินค้าที่ต้องการลบ ^o^ : ")
        shop.remove_product(name)
        
    elif choice == "x":
        print("ออกจากระบบเรียบร้อย ^o^")
        break
    
    else:
        print("เลือกเมนูไม่ถูกต้อง ^o^")
