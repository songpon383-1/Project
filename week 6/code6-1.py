#1
class className :
    name = "I'm MR.Class"
x = className()
print(x.name)



#2
class Car :
    def __init__(self,name,color) :
        self.name =  name
        self.color = color #เก็บชื่อแยกกัน
x = Car("Civic","Blue")
print(x.name)
print(x.color)



#3
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color
    def showCar(self):
       print('Car Information')
       print('Name : ',self.name)
       print('Color : ',self.color)
x = Car('Civic','Blue')
x.showCar()



#4
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color
    def showCar(self):
       print('Car Information')
       print('Name : ',self.name)
       print('Color : ',self.color)
       
Mustang = Car('Mustang' , 'Red')
Mustang.color = 'Black'
Mustang.showCar()

Byd = Car('Byd' , 'White')
Byd.color = 'Pink'
Byd.showCar()



#5
#ปริ้นไม่ได้เพราะเอาออก
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color
    def showCar(self):
       print('Car Information')
       print('Name : ',self.name)
       print('Color : ',self.color)
       
Mustang = Car('Mustang' , 'Red')
del Mustang.color     #เอา color ออกทำให้ปริ้นไม่ได้
print(Mustang.color)



#6 
class Car:
    def __init__(self,name,color) :
       self.name =  name
       self.color = color

    def showCar(self):
        print('Information : Name = ',self.name,' Color =',self.color)
    
class NewCar(Car):
    pass
x = NewCar('Lamborghini' , 'Yellow')
x.showCar()



#7 
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color

    def showCar(self):
        print('Information : Name = ', self.name,'Color =', self.color)

class NewCar(Car):
    def __init__(self,name,color):
        Car.__init__(self,name,color)
        
x = NewCar('Lamborghini' , 'Yellow')
x.showCar()



#8
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color
    def showCar(self):
        print('Information : Name = ',self.name,'Color =',self.color)

class NewCar(Car):
    def __init__(self,name,color):
        Car.__init__(self,name,color)
        super().__init__(name,color) #ใช้ super ในการสืบทอด 
        #super ใช้เรียกเมธอดของคลาสแม่ เวลาที่เราสร้าง คลาสลูกแล้วอยากให้ยังทำงานบางอย่างจากคลาสแม่อยู่
        
x = NewCar('Lamborghini' , 'Yellow')
x.showCar()



#9
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color

    def showCar(self):
        print('Information : Name =', self.name, ', Color =', self.color, ', Gear =', self.gear)

class NewCar(Car):
    def __init__(self,name,color,gear):
        Car.__init__(self,name,color)
        super().__init__(name,color) #ใช้ super ในการสืบทอด
        self.gear = gear
        
x = NewCar('Lamborghini' , 'Yellow' , 'Auto')
x.showCar()



#10
class Car:
    def __init__(self,name,color) :
        self.name =  name
        self.color = color

def showCar(self):
    print('Information : Name = ',self.name,'Color =',self.color)

class NewCar(Car):
    def __init__(self,name,color,gear):
        Car.__init__(self,name,color)
        super().__init__(name,color) #ใช้ super ในการสืบทอด
        self.gear = gear
    def showCar2(self) :
        print(self.name,self.color,self.gear)
        
x = NewCar('Lamborghini' , 'Yellow' , 'Auto')
x.showCar2()