i = 1 
z = int(input('Enter your number : '))
while(i < 13) :
    print(str(z) + 'x' + str(i) + '=' + str(z*i))
    i += 1
    if i == 5 :
        continue