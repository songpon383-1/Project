def standard_arg(arg):
    print(arg)
standard_arg(1)

#ข้าม
#def position_only(arg,/):
#    print(arg)
#position_only(1) #เกิด error เพราะฟังก์ชัน
#position_only(arg = 1) #เป็นการรับค่า position_only ไม่ใช่ keyword

#ข้าม
#def position_only(* , arg):
#    print(arg)
#position_only(arg = 1) #เกิด error เพราะฟังก์ชัน
#position_only(1) #เป็นการรับค่า position_only ไม่ใช่ keyword

def combined(pos_only , / , standard , * , kwd_only):
    print(pos_only , standard , kwd_only)

combined(1,2,kwd_only=3)
combined(1,standard=2 , kwd_only=3)

#เลขชี้กำลัง    
def exponents(base , power):
    return base**power;
print(exponents(2,3))

#วงกลม
def circle_area(area , pie):
    return pie*(area**2)
print(circle_area(3,3.14))

#สามเหลี่ยม
def Triangular_area(hight,base):
    return 1/2*hight*base
print(Triangular_area(12,23))

#สี่เหลี่ยมคางหมู
def trapezoid(hight,a,b):
    return 1/2*hight*(a+b)
print(trapezoid(20,5,5))
