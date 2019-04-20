from music21 import *
from queue import Queue
import dataProcess
import sys
import csv

class PreProcessing:
    def __init__(self,address):
        
        self.s=converter.parse(address)
        self.keyList=[]
        self.dataList=[]
        self.maxM=len(self.s.parts[0].getElementsByClass('Measure'))
        key=self.s.analyze('key')
        for i in range(1,self.maxM):
            self.keyList.append(key)
            self.dataList.append(self.DataExtract(i))
            print(i)
    def KeyCheck(self,bar):
        if  bar<self.maxM-1:
            s1=stream.Stream()
            for i in range(bar,bar+2):
                s1.append(self.s.measure(i))
            key=s1.analyze('key')
            self.keyList[bar]=key
            for i in range(bar-1,self.maxM-1):
                self.keyList[i]=key
    def DataExtract(self,bar):
        print('bar in dataExtract',bar)
        m=self.s.measure(bar)
        d=dataProcess.dataProcess(m,self.keyList[bar-1])
        d.ChordDivide1()
        d.DataProcess()
        return d.output
    def DataUpdate(self):
        for i in range(1,self.maxM):
            self.dataList[i-1]=self.DataExtract(i)
    def WriteToFileKey(self,name):
        with open(name+'key.csv', mode='w') as myFile:
            myWriter=csv.writer(myFile)
            myWriter.writerow([name,'key value'])
            i=0
            for k in self.keyList:
                myWriter.writerow([i,' '+str(k)])
                i=i+1
        print('file name is ',name+'key.csv')
    def WriteToFileData(self,name):
        with open(name+'data.csv', mode='w') as myFile:
            myWriter=csv.writer(myFile)
            myWriter.writerow([name,'data'])
            i=0
            for k in self.dataList:
                myWriter.writerow([i,' '+str(k)])
                i=i+1
