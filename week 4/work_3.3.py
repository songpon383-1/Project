print('ป้อนชื่ออาหารสุดโปรดของคุณ หรือ exit เพื่อออกจากโปรแกรม')

i = 0
r = 0
list = []

while True:
    
    x = str(input(f'อาหารโปรดอันดับที่ {i+1}:'))
    list.append(x)
    
    if x == 'exit' :
        break
    i += 1
list.pop()

for x in list:
    
    print('อาหารโปรดของคุณมีดังนี้ : ' , str(r+1) ,list[r])
    r += 1