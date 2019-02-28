from music21 import *
from const import *
import numpy as np
from copy import deepcopy
import itertools
class dataProcess:
    timeSignature=None
    keyModulus=50
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
        self.outKeyNotes=OUT_KEY_SCALES[self.key.name]
        self.keyValue=0
        self.octave=[0,0,0,0,0,0,0,0,0,0,0,0]
       # print('self.keyScaleMotes',self.keyScaleNotes)
        #print('self.outkeyMotes',self.outKeyNotes)
#self.noteList=KEY_SCALES[k]
        self.apList=[0,0,0,0,0,0,0,0]
        self.output1=deepcopy(self.apList)
        self.output2=deepcopy(self.apList)
        self.measure = m.voicesToParts()

        #remove invalid part(rest)
        self.grid_array,measureCheck=self.InvalidMeasureRemove()
        if not measureCheck: return
        #quarterLength
        self.BeatCount()
        #print(self.octave)
        #check the key 
        self.KeyCheck()
        #print('key value is',self.keyValue)
        
        # processing data
        self.DataProcess()
        '''
        for p in grid_array:
            for n in p:
                test=self.GetNotes(n)

                for ns in self.GetNotes(n):

                   # ns.show('t')
                    for nl in self.noteList:
                        if nl.name==ns.name:
                            index=self.noteList.index(nl)
                            self.apList[index]=self.apList[index]+ns.quarterLength

        sort=np.argpartition(self.apList,-4)[-4:]
        for so in sort:
            if self.apList[so]!=0:
                self.output1[so]=1
        totalQL=0
        for so in sort:
            totalQL=self.apList[so]+totalQL
        #print('total QL ==',totalQL)
        for so in sort:
          #  print('aplist ',so,' is ',self.apList[so])
            if self.apList[so]>totalQL/2:
                self.output2[so]=3
            elif self.apList[so]>totalQL/4:
                self.output2[so]=2
            elif self.apList[so]!=0:
                self.output2[so]=1
         '''       
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

    @staticmethod
    def GetNotes(n):
        if n.isChord: return [cn for cn in n]
        else: return [n]
    def BeatCount(self):
        ts=self.measure.recurse().getElementsByClass(meter.TimeSignature)
        if len(ts)>1:
                self.timeSignature=ts[0]
                self.__class__.timeSignature=self.timeSignature
                #self.timeSignature.show('text') 
        #total beat
        #print('time signature numerator',self.timeSignature.numerator)
        #print('len grid',len(self.grid_array))
        self.totalQL=self.timeSignature.numerator*len(self.grid_array)
        #print('self. total ql',self.totalQL)
        '''
        for p in self.grid_array:
            for c in p:
                for n in self.GetNotes(c):
                    #print('n.name is',n.name)
                    #n.show('text')
                    i=interval.Interval(note.Note('C'),note.Note(n.name))
                    #i.show('text')
                    #print('i name name',i.semitones)
                    self.octave[i.semitones]=self.octave[i.semitones]+n.quarterLength
        '''
    def KeyCheck(self):
        #print('key check')
        #print('grid array is',self.grid_array)
        for p in self.grid_array:
            for c in p:
                for n in self.GetNotes(c):
                    if n.name==self.tonicNote.name or n.name==self.dominantNote.name:
                        self.keyValue=self.keyValue+2*n.quarterLength
                    else:
                        for kn in self.keyScaleNotes:
                            if n.name==kn.name:
                                self.keyValue=self.keyValue+1*n.quarterLength
        self.keyValue=round(self.keyValue/self.totalQL*self.__class__.keyModulus)
    def DataProcess(self):
        #nprint('key name',self.key.name)
        isSpChord=self.CheckChordType(self.grid_array,self.key)
        #print('sp chord',isSpChord)
        if self.key.mode=='major':  
            if not isSpChord:
                # not special chord
                self.apList[-1]=0
                for p in self.grid_array:
                    for c in p:
                        for nc,ns in itertools.product(self.GetNotes(c),self.keyScaleNotes):
                            if nc.name==ns.name:
                                #print('note of chord',nc)
                                #print('self key scale notes',self.keyScaleNotes)
                                index=self.keyScaleNotes.index(ns)
                                self.apList[index]=self.apList[index]+nc.quarterLength
            else:
                self.apList[-1]=1
                for p in self.grid_array:
                    for c in p:
                        for nc,ns in itertools.product(self.GetNotes(c),self.outKeyNotes):
                            if nc.name==ns.name:
                                index=self.outKeyNotes.index(ns)
                                self.apList[index]=self.apList[index]+nc.quarterLength

        elif self.key.mode=='minor':
            printf('minor')

        else:
            print('error key')
            return
        for i,ap in enumerate(self.apList):
            if ap>self.totalQL/2:
                self.output2[i]=3
            elif ap>self.totalQL/4:
                self.output2[i]=2
            elif ap!=0:
                self.output2[i]=1

        #print ('ap list is',self.apList)
        #print ('ouotput is',self.output2)
    def InvalidMeasureRemove(self):
        for n in self.measure.recurse().getElementsByClass('GeneralNote'):
            #n.show('text')
            if n.duration.isGrace:
                self.measure.remove(n, recurse=True)
            
            if n.isRest:
                self.measure.remove(n, recurse=True)
            '''
            for ns in self.GetNotes(n):
                noteCheck=False
                for nn in self.noteList:
                    if nn.name==ns.name:
                        noteCheck=True
                if not noteCheck:
                    self.measure.remove(ns,recurse=True)
                    '''
        # remove invalid part
        grid_array = [[n for n in p.recurse().getElementsByClass('GeneralNote')] for p in self.measure.parts]
        #remove rest parts & rests
        grid_array = [p for p in grid_array if any(not n.isRest for n in p)]
        if not grid_array: return grid_array,False

        return grid_array,True


