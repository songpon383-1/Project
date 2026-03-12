#เปลี่ยนเวลาจาก วัน เป็นชั่วโมง นาที วินาที
print('Converter Program')
day = input('Input number of days : ')
day = int(day)
a = day*24
b = day*24*60
c = day*24*60*60

print( day , 'Day -> Hour : ' , a , 'Hour')
print( day , 'Day -> Minutes : ' , b , 'Minutes')
print( day  , 'Day -> Seconds : ' , c , 'Seconds')