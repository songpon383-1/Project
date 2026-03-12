import os

choice = 0
filename = ''

def menu():
    global choice
    print('Menu\n 1.Open Calculator\n 2.Open Notepad\n 3.Open line\n 4.Exit')
    choice = int(input('Select Menu : '))

def opennotepad():
    filename = r"C:\Windows\System32\notepad.exe"
    print('Memorandum writing %s' % filename)
    os.system(filename)

def opencalculator():
    filename = r"C:\Windows\System32\calc.exe"
    print('Calculate Number %s' % filename)
    os.system(filename)
    
def openline():
    filename = r"C:\Users\ASUS\AppData\Local\LINE\bin\LineLauncher.exe"
    print('Open Line %s' % filename)
    os.system(filename)

while True:
    menu()
    if choice == 1:
        opencalculator()
    elif choice == 2:
        opennotepad()
    elif choice == 3:
        openline()
    else:
        break
