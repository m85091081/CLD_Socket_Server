import requests 
from bs4 import  BeautifulSoup, NavigableString, Tag
from distributed import Client
client = Client('192.168.0.19:8786')

def dataget():
    u = requests.get("http://140.125.45.200:2226/hbase/KZ_web/CarPointReturn_none_car_info.jsp")
    html_doc = u.text
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
    return nlist

def othercar_x_raw(raw):
    rnlist = []
    cnt = 1
    for x in raw :
        if cnt == 1 :
            rnlist.append(x)
            cnt = cnt + 1
        elif cnt == 3 :
            cnt = 1
        else:
            cnt = cnt + 1
    return rnlist

def othercar_y_raw(raw):
    rnlist = []
    cnt = 1
    for x in raw :
        if cnt == 2 :
            rnlist.append(x)
            cnt = cnt + 1
        elif cnt == 3 :
            cnt = 1
        else:
            cnt = cnt + 1
    return rnlist
       
def othercar_X_map(rawdata):
    return int(float(rawdata)*1010000)
    
def othercar_Y_map(rawdata):
    return int(float(rawdata)*1050000)

def othercar_minus(rawdata,minus):
    return rawdata - minus

def resultans():
    other_car_X = client.gather(client.map(othercar_X_map,othercar_x_raw(dataget())))
    other_car_Y = client.gather(client.map(othercar_Y_map,othercar_y_raw(dataget())))
    orign_car_X = []
    orign_car_Y = []
    for x in range(len(other_car_X)-1) :
        orign_car_X.append(other_car_X[0])
        orign_car_Y.append(other_car_Y[0])
    del other_car_X[0]
    del other_car_Y[0]
    X = client.gather(client.map(othercar_minus,other_car_X,orign_car_X))   
    Y = client.gather(client.map(othercar_minus,other_car_Y,orign_car_Y))   
    return [X,Y]
if __name__ == '__main__':
    print(resultans())
