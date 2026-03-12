class Nisit:
    def __init__(self, name , year , branch , gender):
        self.name = input('Enter ชื่อ-นามสกุล > ')
        self.year = input('Enter ชั้นปีที่ > ')
        self.branch = input('Enter สาขา > ')
        self.gender = input('เพศ (ชาย หรือ หญิง) > ')

    def shownisit(self):
        print('\tแนะนำตัว')
        print('ชื่อ-นามสกุล :', self.name)
        print('ชั้นปีที่ :', self.year)
        print('สาขา :', self.branch)
        print('เพศ :', self.gender)
        if self.gender == 'หญิง':
         print('สวัสดีค่ะหนู' , self.name , 'จากสาขา' , self.branch , 'ชั้นปีที่' , self.year, 'เพศ' , self.gender , 'ค่ะ')
        else:
            print('สวัสดีครับผม' , self.name , 'จากสาขา' , self.branch , 'ชั้นปีที่' , self.year, 'เพศ' , self.gender , 'ครับ')

n = Nisit('ทรงพล ประทุมมา', '2', 'คอมพิวเตอร์', 'ชาย')
n.shownisit()
