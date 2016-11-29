import gethtml
rawdata = gethtml.dataget()

def mycar():
    KL_Mycar_X = int(float(rawdata.get('car0')[1])*1010000)
    KL_Mycar_Y = int(float(rawdata.get('car0')[0])*1050000)
    return [KL_Mycar_X,KL_Mycar_Y]

def othercar():
    car = 1
    KL_Othercar_Y = []
    KL_Othercar_X = []
    for x in range(1,5):
        KL_Othercar_Y.append(int(float(rawdata.get('car'+str(car))[0])*1050000)-int(mycar()[1]))
        KL_Othercar_X.append(int(float(rawdata.get('car'+str(car))[1])*1010000)-int(mycar()[0]))
        car = car + 1
    return [KL_Othercar_X,KL_Othercar_Y]


