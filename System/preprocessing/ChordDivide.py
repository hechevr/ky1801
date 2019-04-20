from music21 import *
import numpy as np
import csv
import copy
import itertools

major = ['C', 'C#', 'Cb', 'D', 'D#', 'Db', 'E', 'E#', 'Eb', 'F', 'F#', 'Fb', 'G', 'G#', 'Gb', 'A', 'A#', 'Ab', 'B', 'B#', 'Bb', 'c', 'c#', 'cb', 'd', 'd#', 'db', 'e', 'e#', 'eb', 'f', 'f#', 'fb', 'g', 'g#','gb','a','a#','ab','b', 'b#', 'bb']




class ChordDivide:
    table=[]
    def __init__(self,c,nl):
        self.beatCount=c
        self.noteList=nl
        self.divide=2
        
        if(self.beatCount==9 or self.beatCount==12 or self.beatCount==3):
            self.divide=3
        self.length=self.beatCount/self.divide
        self.subList=[]
        for i in range(0,self.divide):
            self.subList.append([])
        if not self.__class__.table:
            self.__class__.table=self.load_table()

        #self.NoteListCheck()
    @staticmethod
    def load_table():
        table = []
        with open("preprocessing/output.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if (row[0] in major):
                    title = row[0]
                else:
                    row[0] = title + " " + row[0]
                    table.append(row)
        return table
    @classmethod
    def ChordCheck(cls,n):
        ##print("n is",n)
        ##print("cls.table is",cls.table)
        for x,y,z in itertools.product(n,repeat=3):
            xn=x.name
            xn=xn.replace('-','b')
            yn=y.name
            yn=yn.replace('-','b')
            zn=z.name
            zn=zn.replace('-','b')
            notes=xn+' '+yn+' '+zn
            ##print('notes is',notes)
            for t in cls.table:
                if notes in t:
                    return True
        return False
    def NoteListCheck(self):
        ##print("in note list check")
        for n in self.noteList:
            n.show('text')
            #print('offset',n.offset)
            
            np=n.quarterLength+n.offset
            #print('np is',np)
            #print('self.length',self.length)

    def DivideToSub(self):
        for n in self.noteList:
            np=n.quarterLength+n.offset
            for i in range(0,self.divide): 
                if n.offset<self.length*(i+1) and n.offset>=self.length*(i):
                    if np>self.length*(i+1):
                        temNote=copy.deepcopy(n)
                        temNote.quarterLength=self.length*(i+1)-n.offset
                        if temNote.quarterLength>0:
                            self.subList[i].append(temNote)
                            ##print("temNote1 quarterlength",temNote.quarterLength)

                            ##print('1')
                    else:
                        ##print("n quarterlength",n.quarterLength)
                        self.subList[i].append(n)
                        ##print('2')

                elif np<self.length*(i+1) and np>=self.length*(i):
                    if n.offset<self.length*(i):
                        temNote=copy.deepcopy(n)
                        temNote.quarterLength=np-self.length*(i)
                        if temNote.quarterLength>0:
                            self.subList[i].append(temNote)
                            ##print("temNote3 quarterlength",temNote.quarterLength)

                            ##print('3')
                    else:
                        ##print('4')
                        ##print('n quarterlength',n.quarterLength)
                        self.subList[i].append(n)
                ##print('sub list ',i,' is ',self.subList[i])
                '''
        for sl in self.subList:
            #print("sub list ",sl)
                '''
        
