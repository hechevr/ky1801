from music21 import *
from preprocessing.const import *
import numpy as np
from copy import deepcopy
import csv
import queue
import itertools
import preprocessing.ChordDivide as CD
major = ['C', 'C#', 'Cb', 'D', 'D#', 'Db', 'E', 'E#', 'Eb', 'F', 'F#', 'Fb', 'G', 'G#', 'Gb', 'A', 'A#', 'Ab', 'B', 'B#', 'Bb', 'c', 'c#', 'cb', 'd', 'd#', 'db', 'e', 'e#', 'eb', 'f', 'f#', 'fb', 'g', 'g#','gb','a','a#','ab','b', 'b#', 'bb']


class dataProcess:
    timeSignature=None
    keyModulus=50
    baseC=note.Note('c')
    table=[]
    def __init__(self,m,k): 
        # circle the chord
        # decide the chord type for each chord
        self.key=k 
        self.scale=k.getScale(self.key.mode)
        self.tonicNote=self.scale.getTonic()
        self.dominantNote=self.scale.getDominant()
        self.timeSignature=self.__class__.timeSignature
        self.pitchs=self.scale.getPitches()
        self.keyScaleNotes=[note.Note(p.name) for p in self.pitchs]
        self.keyScaleNotes=self.keyScaleNotes[0:-1]
        # self.outKeyNotes=OUT_KEY_SCALES[self.key.name]
        #sekf,test12Scale=[note.Note(p.name) for p in ]
        self.keyValue=0
        self.octave=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.test12DList=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.divideGrid=[]
       # #print('self.keyScaleMotes',self.keyScaleNotes)
        self.noteList=[]
        ##print('self.outkeyMotes',self.outKeyNotes)
#self.noteList=KEY_SCALES[k]
        self.apList=[0,0,0,0,0,0,0,0]
        self.output1=deepcopy(self.apList)
        self.output2=deepcopy(self.apList)
        self.output=[]
        self.measure=m
        self.totalQL=0
        #remove invalid part(rest)
        self.grid_array,measureCheck=self.InvalidMeasureRemove()
        if not measureCheck: return
        self.GetNoteList()
        #self.NoteListCheck()
        ##print("self.grid is",self.grid_array)
        ##print("self.note list is",self.noteList)
        self.BeatCount()
        self.measure = m.voicesToParts()
        #self.KeyCheck()
        ##print('key value is',self.keyValue)
        
        # processing data
             
    def GetNoteList(self):
        for p in self.grid_array:
            for c in p:
                for nc in self.GetNotes(c):
                    self.noteList.append(nc)

    def NoteListCheck(self):
        for n in self.noteList:
            n.show("text")
            #print(' offset ',n.offset)
            #print('quarterlength',n.quarterLength)
        # get the leveled ap list 
    def CheckChordType(self,data,key): 
        if key.mode== 'major':
            spNote=CHORD_TYPE_NOTES[key.name][0]
            for p in data:
                for c in p:
                    for n in self.GetNotes(c):
                        if n.name ==spNote.name:
                            return True            
            return False     
    def Test12D(self):
        testList=[0,0,0,0,0,0,0,0,0,0,0,0]
        for p in self.grid_array:
            for c in p:
                for nc in self.GetNotes(c):
                    tNote=note.Note(nc.name)
                    inter=interval.notesToChromatic(self.__class__.baseC,tNote)
                    ##print('inter is ',inter)
                    index=inter.semitones
                    ##print('index is ',index)
                    keyInter=interval.notesToChromatic(self.__class__.baseC,self.tonicNote)
                    keyIndex=keyInter.semitones
                    index=index-keyIndex
                    if index<0:
                        index=index+12
                    if index>12:
                        index=index-12
                    testList[index]=testList[index]+nc.quarterLength
        for i,tl in enumerate(testList):
            testList[i]=round(tl/self.totalQL,2)
        ##print('test list',testList)
        self.test12DList=testList

        return testList
    @staticmethod
    def GetNotes(n):
        if n.isChord:
            for cn in n:
                cn.offset=n.offset
            return [cn for cn in n]
        else: return [n]
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

   
    def BeatCount(self):
        #print('in beat cocunt')
        #self.measure.show('text')
        ts=self.measure.recurse().getElementsByClass(meter.TimeSignature)
        #print('ts',ts)
        
        if len(ts)>1:
            #print('ts length >1')
            self.timeSignature=ts[0]
            self.__class__.timeSignature=self.timeSignature
        #print('time signature',self.timeSignature)
        if not self.__class__.table:
            self.__class__.table=self.load_table()
        ##print("table is",table)

        '''
        self.totalQL=0
        
        for p in self.grid_array:
            for c in p:
                for n in self.GetNotes(c):
                    ##print('n.name is',n.name)
                    #n.show('text')
                    i=interval.Interval(note.Note('C'),note.Note(n.name))
                    #i.show('text')
                    ##print('i name name',i.semitones)
                    self.octave[i.semitones]=self.octave[i.semitones]+n.quarterLength
    

    
    '''
    def ChordDivide1(self):
        #1.find all notes,get beat number
        #2.check if multi chords
        #3.split the measure according to beats
        beatCount=self.__class__.timeSignature.beatCount
        
        cd=CD.ChordDivide(beatCount,self.noteList)
        
        stack=[]
        stack.append(cd)


        while not len(stack)==0:          
            front=stack.pop()
            front.DivideToSub()
            #print("front notelist",front.noteList)
            stackIndex=0
            for sl in front.subList:
                #print("sl is",sl)
                #print(CD.ChordDivide.ChordCheck(sl))
                ##print("beat count",front.beatCount)
                CDcheck=CD.ChordDivide.ChordCheck(sl)

                if CDcheck ==True and front.beatCount>1:
                    cds=CD.ChordDivide(front.length,sl)
                    stack.append(cds)
                    stackIndex=stackIndex+1
                else: 
                    #print('add front notelist',front.noteList)
                    self.divideGrid.append(front.noteList)
                    while(stackIndex>0):
                        test=stack.pop()
                        stackIndex=stackIndex-1
                    break
                ##print("self divide grid after append",self.divideGrid) 
        self.divideGrid.reverse()
        #print("self divide grid is",self.divideGrid)
    def KeyCheck(self):
        #print('key check')
        ##print('grid array is',self.grid_array)
        for p in self.grid_array:
            for c in p:
                for n in self.GetNotes(c):
                    if n.name==self.tonicNote.name or n.name==self.dominantNote.name:
                        self.keyValue=self.keyValue+2*n.quarterLength
                        self.totalQL=self.totalQL+n.quarterLength
                    else:
                        for kn in self.keyScaleNotes:
                            if n.name==kn.name:
                                self.keyValue=self.keyValue+1*n.quarterLength
                                self.totalQL=self.totalQL+n.quarterLength
        self.keyValue=round(self.keyValue/self.totalQL*self.__class__.keyModulus)
        #print('in key check self ql',self.totalQL)

    def DataProcess(self):
        #print("self.divide grid",self.divideGrid)
        for comp in self.divideGrid:    
            totalQL=0
            for n in comp:
                totalQL=totalQL+n.quarterLength
            testList=[0,0,0,0,0,0,0,0,0,0,0,0]
            #print('totalQL is',totalQL)
                
            for n in comp:
                tNote=note.Note(n.name)
                inter=interval.notesToChromatic(self.__class__.baseC,tNote)
                ##print('inter is ',inter)
                index=inter.semitones
                ##print('index is ',index)
                keyInter=interval.notesToChromatic(self.__class__.baseC,self.tonicNote)
                keyIndex=keyInter.semitones
                index=index-keyIndex
                if index<0:
                    index=index+12
                if index>12:
                    index=index-12
                testList[index]=testList[index]+n.quarterLength
                ##print("test list for",n.name," ","length is ",n.quarterLength,"offset is ",n.offset," ",testList)
            for i,tl in enumerate(testList):
                testList[i]=round(tl/totalQL,2)
            ##print('test list',testList)
            self.output.append(testList)
                
        #print("self.output",self.output)
    def InvalidMeasureRemove(self):
        for n in self.measure.recurse().getElementsByClass('GeneralNote'):
            if n.duration.isGrace:
                self.measure.remove(n, recurse=True)
            if n.isRest:
                self.measure.remove(n, recurse=True)
            # remove invalid part
        grid_array = [[n for n in p.recurse().getElementsByClass('GeneralNote')] for p in self.measure.parts]
        #remove rest parts & rests
        #grid_array = [p for p in grid_array if any(not n.isRest for n in p)]
        if not grid_array: return grid_array,False

        return grid_array,True


