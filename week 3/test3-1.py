thisdict = {
    'name' : 'Songpon Prathumma',    #key 
    'year' : '2006',
    'number id' : '673050383-1'
}
thisdict.pop('year') #เป็นการลบข้อมูลที่มีของ key เป็น year
thisdict.popitem() # เป็นการลบข้อมูลที่เพิ่มล่าสุด ลบ number id 
print(thisdict)