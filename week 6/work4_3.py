NAME = []
PTS = []
TIME = []
HIT_FACTOR = [] #ตัวคูณประสิทธิภาพการยิง
STATE_POINTS = [] #คะแนนที่ปรับตามมาตรฐาน
STATE_PERCENT = [] #เปอร์เซ็นต์เทียบกับผู้ที่ทำได้ดีที่สุด

import datetime # นำเข้าโมดูล datetime เพื่อใช้เรียกเวลาปัจจุบัน

while True:
    print('Show score enter [1] :\nEnter data [2] :\nExit [x]')
    print('{0:-<80}'.format(''))
    user1 = input('Enter : ')

    # แสดงผล
    if user1 == '1':
        while True:
            print('{0:-<80}'.format(''))
            data = ['No.' , 'PTS' , 'TIME' , 'Name' , 'HIT FACTOR' , 'STATE POINTS' , 'STATE PERCENT']
            print('Shotgun Sunday Training 2021')
            now = datetime.datetime.now()
            print(f'{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}')
            print('{0:-<80}'.format(''))
            print(f'{data[0]:<5}{data[1]:<8}{data[2]:<8}{data[3]:<20}{data[4]:<15}{data[5]:<15}{data[6]:<15}')
            print('{0:-<80}'.format(''))


            STATE_POINTS.clear()
            STATE_PERCENT.clear()
            if HIT_FACTOR:
                max_hit = max(HIT_FACTOR)
                max_pts = max(PTS)
                for hf in HIT_FACTOR:
                    sp = (hf / max_hit) * max_pts
                    pct = (hf / max_hit) * 100
                    STATE_POINTS.append(sp)
                    STATE_PERCENT.append(pct)


            list = []
            for i in range(len(NAME)):
                list.append((NAME[i] , PTS[i] , TIME[i] , HIT_FACTOR[i] , STATE_POINTS[i] , STATE_PERCENT[i]))

            list.sort(key=lambda x: (-x[1] , x[2])) 
            #sortเรียงลำดับสมาชิกใน list 
            #key ใช้กำหนดฟังก์ชันที่จะแปลง
            #ใช้สร้าง ฟังก์ชันแบบสั้น ๆ

            for i , d in enumerate(list , start=1): #เอาไว้ใช้ วนลูป พร้อมกับได้ index ของข้อมูลนั้น ๆ
                print(f'{i:<5}{d[1]:<8}{d[2]:<8}{d[0]:<20}{d[3]:<15.2f}{d[4]:<15.2f}{d[5]:<15.2f}')

            print('Exit [x] : ')
            Exit = input('Enter : ')
            if Exit == 'x':
                print('{0:-<80}'.format(''))
                break

    # กรอกข้อมูล
    elif user1 == '2':
        while True:
            print('{0:-<80}'.format(''))
            name = input('Enter name contestant : ')
            NAME.append(name)

            pts = int(input('Enter PTS contestant : '))
            PTS.append(pts)

            time = int(input('Enter TIME : '))
            TIME.append(time)
            
            hit_factor = pts / time
            HIT_FACTOR.append(hit_factor)
            
            print('{0:-<80}'.format(''))
            print('Exit [x] : \nFill in the information [a] :')
            Exit = input('Enter : ')

            if Exit == 'a':
                continue
            elif Exit == 'x':
                break

    elif user1 == 'x':
        print('ขอบคุณที่ใช้บริการ ^o^')
        break