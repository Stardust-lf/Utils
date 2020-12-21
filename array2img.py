from PIL import Image
import csv
import cv2 as cv
import random
import numpy as np
def readData():
    lix = list()
    liy = list()
    f = open('predictfin.csv', 'rt').readlines()
    d = csv.reader(f)
    for line in d:
        linflo = list()
        for ite in line:
            print(ite)
            linflo.append(float(ite))
        lix.append(linflo[:-2])
        liy.append(linflo[30])
        pass
    return (lix,liy)
data = readData()
lixt = list()
lixf = list()

for i in range(2785):
    print(i)
    if data[1][i] == 1:
        lixt.append(data[0][i])
        pass
    else:
        lixf.append(data[0][i])
        pass
    pass

for i in range(len(lixt)):
    numarr = np.array(lixt[i] + lixt[i] + lixt[i])
    RGBimage = numarr.reshape(1,29,3)
    cv.imwrite('bntestImg/predict/getDisease/'+ str(i+1) + '.jpg',RGBimage)
    pass
for i in range(len(lixf)):
    numarr = np.array(lixf[i] + lixf[i] + lixf[i])
    RGBimage = numarr.reshape(1,29,3)
    cv.imwrite('bntestImg/predict/notGetDisease/'+ str(i+1) + '.jpg',RGBimage)