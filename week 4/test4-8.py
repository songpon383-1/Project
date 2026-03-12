def Introduce (name, *hobby, **address) :
    print("Hello, I am " +name+",")
    print("My address : ")
    for kw in address :
        print(kw + ":" + address [kw])
    print("My hobby : ")
    for arg in hobby :
        print(arg)

Introduce("P","Sport","Music","game", province = "Khon Kaen", nation = "Thailand")