import requests 
from bs4 import  BeautifulSoup, NavigableString, Tag
from distributed import Client
client = Client()
u = requests.get("http://140.125.45.200:2226/hbase/KZ_web/CarPointReturn_none_car_info.jsp")
html_doc = u.text

def dataget():
    soup = BeautifulSoup(html_doc, 'html.parser')
    sbody = soup.body
    rawdata = []
    nlist =[]
    ndict = {}
    i = 0
    for br in sbody.findAll('br'):
        next = br.nextSibling
        if not (next and isinstance(next,NavigableString)):
            continue
        next2 = next.nextSibling
        if next2 and isinstance(next2,Tag) and next2.name == 'br':
            text = str(next).strip()
            if text:
                rawdata.append(text)
    for t in range(14,29):
        nlist.append(rawdata[t])
    for x,y,z in zip(nlist[0::3],nlist[1::3],nlist[2::3]) :
        ndict['car'+str(i)] = [x,y,z]
        i = i + 1
    return ndict


def carcomp(rawdata):
    KL_Mycar_X = int(float(rawdata.get('car0')[1])*1010000)
    KL_Mycar_Y = int(float(rawdata.get('car0')[0])*1050000)
    return [KL_Mycar_X,KL_Mycar_Y]

def othercar(mycar,rawdata):
    car = 1
    KL_Othercar_Y = []
    KL_Othercar_X = []
    for x in range(1,5):
        KL_Othercar_Y.append(int(float(rawdata.get('car'+str(car))[0])*1050000)-int(mycar[1]))
        KL_Othercar_X.append(int(float(rawdata.get('car'+str(car))[1])*1010000)-int(mycar[0]))
        car = car + 1
    return [KL_Othercar_X,KL_Othercar_Y]

html = client.submit(dataget)
anscar = client.submit(carcomp,html)
ans = client.submit(othercar,anscar,html)

print(ans.result())
