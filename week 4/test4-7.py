def Introduce(names) : #names = Arguments
    print("Hello, I'm " + names)
Introduce("Python") #ถูกนำไปเก็บไว้ที่ Arguments names

def Introduce(names) :
    print("Hello, I'm " + names)
A = input('Enter your name : ')
Introduce(A) 

def Introduce(province , nation = 'Thailand') :
    print("Hello, I come from " + province + "," + nation)
Introduce("Khon Kaen","USA")

def Introduce(province , nation) :
    print("Hello, I come from " + province + "," + nation)
nation = input('Enter your nation :')
Introduce("Khon Kaen",nation) 

def Introduce(arg1, arg2 = 'com' , arg3 = 'ed' , arg4 = 'kku') :
    print("Hello, I am "+arg1+", "+arg2+" "+arg3+" "+arg4)
    
#ตัวอย่างที่ไม่ได้!!!
Introduce() #missing 1 required argment
Introduce(arg1 = "Python" , "CMU") #non-kwarg after kwarg
Introduce("Python 2" , arg1 = "Python 3") #same argument
Introduce(arg99 = "CMU") #unknow kwarg

def Introduce (name, *hobby, **address) :
    print("Hello, I am " +name+",")
    print("My address : ")
    for kw in address :
        print(kw + ":" + address [kw])
    print("My hobby : ")
    for arg in hobby :
        print(arg)

Introduce("P","Sport","Music","game", province = "Khon Kaen", nation = "Thailand")