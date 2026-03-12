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