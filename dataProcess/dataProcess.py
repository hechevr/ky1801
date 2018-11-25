from music21 import *
from const import *
import numpy as np
from copy import deepcopy
class dataProcess:
    def __init__(self,m,k):
        self.noteList=KEY_SCALES[k]
        self.apList=[0,0,0,0,0,0,0]
        self.output=deepcopy(self.apList)
        self.measure = m.voicesToParts()
        for n in self.measure.recurse().getElementsByClass('GeneralNote'):
            if n.duration.isGrace:
                self.measure.remove(n, recurse=True)
            #print('input n is',n)
            for ns in self.GetNotes(n):
                noteCheck=False
                for note in self.noteList:
             #       print('before',ns)
                    if note.name==ns.name:
                      #  print('in name check',note.name)
                       # print(ns.name)
                        noteCheck=True
                if not noteCheck:
                    #print('remove',ns.name)
                    self.measure.remove(ns,recurse=True)
        # remove invalid part
        grid_array = [[n for n in p.recurse().getElementsByClass('GeneralNote')] for p in self.measure.parts]
        #print('grid before is',grid_array) 
        #remove rest parts & rests
        grid_array = [p for p in grid_array if any(not n.isRest for n in p)]
        if not grid_array: return
        #print('grid is ',grid_array) 
        for p in grid_array:
            for n in p:
                test=self.GetNotes(n)
               # print('test is ',te:st)
                for ns in self.GetNotes(n):
                #    print('ns is ',ns)
                    ns.show('t')
                    for nl in self.noteList:
                        if nl.name==ns.name:
                            index=self.noteList.index(nl)
                            self.apList[index]=self.apList[index]+ns.quarterLength
        #print('self aplist is ',self.apList) 
        sort=np.argpartition(self.apList,-4)[-4:]
        for so in sort:
            if self.apList[so]!=0:
                self.output[so]=1
    @staticmethod
    def GetNotes(n):
        if n.isChord: return [cn for cn in n]
        else: return [n]

