a = 60 
b = 13
c = 0

c = a & b #and ให้ค่า bit เป็น 1 ถ้า bit ทั้งคู่เป็น 1
print(c)

c = a | b #or ให้ค่า bit เป็น 1 ถ้า bit ใด bit หนึ่งเป็น 1
print(c)

c = a ^ b #xor ให้ค่า bit เป็น 1 ถ้า bit ใด bit หนึ่งเป็น 1 และอีก bit เป็น 0
print(c)

c = ~a
print(c) #not กลับ bit ทั้งหมดจาก 1 เป็น 0 และจาก 0 เป็น 1

c = a << 2 #zero left shift เติม 0 ด้านขวา และตัด bit ที่เป็น 0 ด้านซ้าย
print(c)

c = a >> 2 #singed right shift เติม 0 ด้านซ้าย และตัด bit ที่เป็น 0 ด้านขวา
print(c)