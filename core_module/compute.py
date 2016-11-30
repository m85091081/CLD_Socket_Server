import gethtml
from distributed import Client
client = Client()
rawdata = gethtml.dataget()

def carcomp(me):
    print(me)
    KL_Mycar_X = int(float(rawdata.get('car0')[1])*1010000)
    KL_Mycar_Y = int(float(rawdata.get('car0')[0])*1050000)
    return [KL_Mycar_X,KL_Mycar_Y]

def othercar(mycar):
    car = 1
    KL_Othercar_Y = []
    KL_Othercar_X = []
    for x in range(1,5):
        KL_Othercar_Y.append(int(float(rawdata.get('car'+str(car))[0])*1050000)-int(mycar[1]))
        KL_Othercar_X.append(int(float(rawdata.get('car'+str(car))[1])*1010000)-int(mycar[0]))
        car = car + 1
    return [KL_Othercar_X,KL_Othercar_Y]

anscar = client.submit(carcomp,'1')
ans = client.submit(othercar,anscar)

print(ans.result())
