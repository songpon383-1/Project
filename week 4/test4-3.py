i = 1 
z = int(input('Enter your number : '))
while(i < 12) :
    i += 1
    if i != 5 :
        continue
    print(str(z) + 'x' + str(i) + '=' + str(z*i))