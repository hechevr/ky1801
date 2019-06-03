from music21 import *
from queue import Queue
import dataProcess
import sys
import csv

dataList=[]
keyValueList=[]
keyList=[]
testDataList=[]
xmlName=['Mozart1.musicxml','Mozart.mxl','Von.mxl','thehf.mxl']
DirectoryName=['','','Von/','thehf/']
directory='../data/Mozart2/'
KEY_THRE=50
fileNumber=int(sys.argv[2])
dataDirectory='../data/'
dataFile=dataDirectory+DirectoryName[fileNumber]+xmlName[fileNumber]
#testing function for key value data
def WriteToFileKey(name):
    with open(name+'keyi.csv', mode='w') as myFile:
        myWriter=csv.writer(myFile)
        myWriter.writerow([name,'key value'])
        i=0
        for k in keyValueList:
            myWriter.writerow([i,' '+str(k)])
            i=i+1
def WriteToFileData(name):
    with open(name+'data.csv', mode='w') as myFile:
        myWriter=csv.writer(myFile)
        myWriter.writerow([name,'data'])
        i=0
        for k in dataList:
            myWriter.writerow([i,' '+str(k)])
            i=i+1
#testing function for key value            
def KeyProcess(kList,vList,score,key):
    q=Queue()
    kList=CheckConsistence(kList,vList,key)
#testing function for key value
def CheckConsistence(kList,vList,key):
    for i in range(1, len(vList)-2):
        if vList[i-1]>50 and vList[i+1]>50:
            vList[i] =vList[i]+20
        elif vList[i-1]<50 and vList[i+1]<50:
            vList[i]=vList[i]-20
    for i,v in enumerate(vList):
        if v>KEY_THRE:
            kList[i]=key
    return vList,kList




s=converter.parse(dataFile)
key=key.Key(sys.argv[1])
key.show('text')
measureNumber=len(s.parts[0].getElementsByClass('Measure'))

for i in range(1, measureNumber):
    m=s.measure(i)
    d=dataProcess.dataProcess(m,key)
    d.ChordDivide1()
    d.DataProcess()
    dataList.append(d.output)
Name=dataFile[:-4]
WriteToFileData(Name)
