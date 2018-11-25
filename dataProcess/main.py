from music21 import *
import dataProcess
import sys

xmlName=['Mozart1.musicxml']
s=converter.parse(xmlName[0])
'''
#s.measure(7).show('t')
m=dataProcess.dataProcess(s.measure(7),'C')
t=m.output
print(t)

'''
measureNumber=len(s.parts[0].getElementsByClass('Measure'))
dataList=[]
for i in range(1,measureNumber+1):
    m=s.measure(i)
    d=dataProcess.dataProcess(m,'C')
    dataList.append(d.output)
    
print(dataList)
f=open('Mozart1.txt','w')
for i,l in enumerate(dataList):
    f.write('bar number:{},{}\n'.format(i+1,l))
    
