'''
Purpose:
        Given several notes, return the correct chord
        using ROman numeral to express the chored
'''

import sys
import re
from enum import Enum

#global variable

class ChordNum(Enum):
    triad=3
    seventhChord=4
   
class ModeType(Enum):
    Major='major'
    Minor='minor'
class Note(Enum):
    C='C'
    C_s='C#'
    D_f='Db'
    D='D'
    D_s='D#'
    E_f='Eb'
    E='E'
    F='F'
    F_s='F#'
    G_f='Gb'
    G='G'
    G_s='G#'
    A_f='Ab'
    A='A'
    A_s='A#'
    B_f='Bb'
    B='B'

#music interval class
class M_I(Enum):
    M3=4
    m3=3
    M2=2
    m2=1


class Chord():
    def __init__(self,root=None,num=None,type=None,notes=[],intervals=[]):
        self.root=root
        self.type=type
        self.num=num
        self.notes=notes
        if self.root!=None:
              self.addNotes(root)
        self.intervals=intervals
    def addInterval(self, interval):
        self.intervals.append(interval)
    def addNotes(self,note):
        self.notes.append(note)
    def __del__(self):
        print ('deleted')

class Mode():
    MajorScaleTable=[M_I.M2,M_I.M2,M_I.m2,M_I.M2,M_I.M2,M_I.M2,M_I.m2]
    MinorScaleTable=[M_I.M2,M_I.m2,M_I.M2,M_I.M2,M_I.m2,M_I.M2,M_I.M2]
    def __init__(self,root,type):
        self.root=root
        self.type=type
        
class ChordType(Enum):
    Major='maj'
    Minor='m'
    Dominant='dom'
    Aug='aug'
    Dim='dim'
    Sus='sus'
    Null='no'
    Minorf5='mb5'

# chord table
augChordTable={1:M_I.M3,2:M_I.M3,3:M_I.M2}
majorChordTable={1:M_I.M3,2:M_I.m3,3:M_I.M3,4:M_I.m3,5:M_I.m3,6:M_I.M3}
minorChordTable={1:M_I.m3,2:M_I.M3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
dominantCHordTable={1:M_I.M3,2:M_I.m3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
noteTable={Note.C:1,Note.D_f:2,Note.D:3,Note.E_f:4,Note.E:5,Note.F:6,Note.G_f:7,Note.G:8,Note.A_f:9,Note.A:10,Note.B_f:11,Note.B:12}   
flatCheckTable={Note.C:1,Note.D:2,Note.E:3,Note.F:4,Note.G:5,Note.A:6,Note.B:7} 
flatList=[Note.D_f,Note.E_f,Note.G_f,Note.A_f,Note.B_f]
originList=[Note.D,Note.E,Note.G,Note.A,Note.B]
sharpList=[Note.C_s,Note.D_s,Note.F_s,Note.G_s,Note.A_s]
#roman number table    
R_N_table={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7}
# major mode triad table
MajModeTtable={1:ChordType.Major,2:ChordType.Minor,3:ChordType.Minor,4:ChordType.Major,5:ChordType.Major,6:ChordType.Minor,7:ChordType.Dim}
#major mode seventh table
MajModeStable={1:ChordType.Major,2:ChordType.Minor,3:ChordType.Minor,4:ChordType.Major,5:ChordType.Dominant,6:ChordType.Minor,7:ChordType.Minorf5}
#minor mode triad table
MinModeTtable={1:ChordType.Minor,2:ChordType.Dim,3:ChordType.Major,4:ChordType.Minor,5:ChordType.Minor,6:ChordType.Major,7:ChordType.Major}
#minor mode seventh table
MinModeTtable={1:ChordType.Minor,2:ChordType.Minorf5,3:ChordType.Major,4:ChordType.Minor,5:ChordType.Minor,6:ChordType.Major,7:ChordType.Dominant}
#main function
print('input \'quit\' to quit')
while input()!='quit':
    print('Choose your identification mode\n 1.Note to chord\n 2.Chord to note')
    mode=input()

    while mode!='1' and mode!='2':
        print('Wrong input. Please input the correct answer')
        mode=input()

    if mode=='1':
        print('in note to chord mode\n input your notes')
        inputValue=input()
        outputChord=Chord()
        notes=inputValue.split()
        for inputNote in notes:
            for note in Note:
                if inputNote==note.value:
                    outputChord.addNotes(note)
        outputChord.root=outputChord.notes[0]
        print(outputChord.notes)
        if len(notes)==3:
            outputChord.num=ChordNum.triad
        elif len(notes)==4:
            outputChord.num=ChordNum.seventhChord
        firstNote=outputChord.root
        secondNote=firstNote
        for note in outputChord.notes:
            secondNote=note
            if secondNote==firstNote:
                continue
            else:
                if noteTable[secondNote]<noteTable[firstNote]:
                    indexDif=noteTable[secondNote]+12-noteTable[firstNote]
                else:
                    indexDif=noteTable[secondNote]-noteTable[firstNote]
                print('index dif ',indexDif)
                for musicInterval in M_I:
                    if indexDif==musicInterval.value:
                        outputChord.addInterval(musicInterval)
                        print('here')
                firstNote=secondNote
        print(outputChord.intervals)
        chordTypeCheck=True
        for interval,chordInterval in zip(outputChord.intervals,MajModeTtable):
            if interval!=chordInterval:
                chordTypeCheck=False
        if chordTypeCheck==True:
            outputChord.type=ChordType.Major

        chordTypeCheck=True
        for interval,chordInterval in zip(outputChord.intervals,MinModeTtable):
            if interval!=chordInterval:
                chordTypeCheck=False
        if chordTypeCheck==True:
            outputChord.type=ChordType.Minor

        chordTypeCheck=True
        for interval,chordInterval in zip(outputChord.intervals,augChordTable):
            if interval!=chordInterval:
                chordTypeCheck=False
        if chordTypeCheck==True:
            outputChord.type=ChordType.Aug

        chordTypeCheck=True
        for interval in outputChord.intervals:
            if interval!=3:
                chordTypeCheck=False
        if chordTypeCheck==True:
            outputChord.type=ChordType.Dim
    elif mode=='2':
        print('in chord to note mode\n input your chord Mode')
        inputValue=input()
        if(inputValue==inputValue.lower()):
            ModeType=ModeType.Minor
            inputValue=inputValue.upper()
        elif(inputValue==inputValue.upper()):
            ModeType=ModeType.Major
        #print(inputValue)
        #print(ModeType)
        for note in Note:
            #print(note)
            if note.value==inputValue:
                ModeRoot=note
        inputMode=Mode(ModeRoot,ModeType)
    
        print('input your chord discription')
        inputValue=input()
        for roman in R_N_table:
            if roman==inputValue:
                inputRoman=R_N_table[roman]
        i=1
        chordRoot=inputMode.root
        noteIndex=noteTable[chordRoot]
  
        while i<inputRoman:
            if(inputMode.type==ModeType.Major):
                noteIndex=noteIndex+Mode.MajorScaleTable[i-1].value
            elif inputMode.type==ModeType.Minor:
                noteIndex=noteIndex+Mode.MinorScaleTable[i-1].value
            i=i+1
            if noteIndex>12:
                noteIndex=noteIndex-12
        print('note index is ',noteIndex)
        for note in noteTable:
            if noteTable[note]==noteIndex:
                chordRoot=note
        print(chordRoot)
        print('Choose your chord mode\n1.triad\n 2.seventh chord')
        inputValue=input()
        if inputValue=='1':
            if(inputMode.type==ModeType.Major):
                chordType=MajModeTtable[inputRoman]
                inputChord= Chord(chordRoot, ChordNum.triad,chordType)
                #print('inputchord ',inputChord.notes)
            elif(inputMode.type==ModeType.Minor):
                chordType=MinModeTtable[inputRoman]
                inputChord= Chord(chordRoot, ChordNum.triad,chordType)
        elif inputValue=='2':
            if(inputMode.type==ModeType.Major):
                chordType=MajModeStable[inputRoman]  
                inputChord= Chord(chordRoot,ChordNum.seventhChord,chordType)
            elif(inputMode.type==ModeType.Major):
                chordType=MinModeStable[inputRoman]  
                inputChord= Chord(chordRoot,ChordNum.seventhChord,chordType)
            
        print('input chord type is ',inputChord.type)
        #find all notes
        firstNote=inputChord.root
        secondNote=firstNote
        for i in range (inputChord.num.value-1):
            
            firstIndex=noteTable[firstNote]
            if(inputChord.type==ChordType.Major):    
                secondIndex=firstIndex+majorChordTable[i+1].value
                print('second index',secondIndex)
            if(inputChord.type==ChordType.Minor or inputChord.type==ChordType.Minorf5):
                secondIndex=firstIndex+minorChordTable[i+1].value
            if(inputChord.type==ChordType.Dominant):
                secondIndex=firstIndex+dominantCHordTable[i+1].value
            if(inputChord.type==ChordType.Dim):
                secondIndex=firstIndex+3
            if(inputChord.type==ChordType.Aug):
                secondIndex=firstIndex+augChordTable[i+1].value
            if(secondIndex>12):
                secondIndex=secondIndex-12
            for note in noteTable:
                if noteTable[note]==secondIndex:
                    secondNote=note
            inputChord.addNotes(secondNote)
            #print('after add note',inputChord.notes)
            firstNote=secondNote
           # print("list ",inputChord.notes)
       # check the minor flat 5  
        if inputChord.type==ChordType.Minorf5:
            temIndex=noteTable[inputChord.notes[2]]
            for note in noteTable:
                if noteTable[note]== temIndex-1:
                    inputChord.notes[2]=note
                    
                print('here')
        # check sharp or flat expression
        # checkNotes is iiiiiiiiiineed to change, changenote after change
        checkNotes=[]
        changeNotes=[]
        lastNote=inputMode.root
        corIndex=flatCheckTable[inputMode.root]+inputRoman-1
        if corIndex>7:
            corIndex=corIndex-7
        for note in flatCheckTable:
            print('here')
            if flatCheckTable[note]==corIndex:
                corNote=note
        for i,j,k in zip(flatList,originList,sharpList):
            if i ==inputChord.root:
                if j!=corNote:
                    checkNotes.append(inputChord.root)
                    changeNotes.append(k) 
        lastNote=corNote
        for note in inputChord.notes:
            checkNote=note
            if checkNote==lastNote:
                continue
            noteFlat=False
            for flatNote in flatList:
                if checkNote==flatNote:
                    noteFlat=True
            if noteFlat==True:
                #correct note for flat note
                corIndex=flatCheckTable[lastNote]+2
                if corIndex>7:
                    corIndex=corIndex-7
                for note1 in flatCheckTable:
                    if flatCheckTable[note1]==corIndex:
                        corNote=note1
                for i,j,k in zip(flatList,originList,sharpList):
                    if i ==note:
                        if j!=corNote:
                            checkNotes.append(note)
                            changeNotes.append(k)

            lastNote=corNote
            print('last note',lastNote)
        for i in range (len(inputChord.notes)):
            for note1,note2 in zip(checkNotes,changeNotes):
                if note1==inputChord.notes[i]:
                    inputChord.notes[i]=note2
        print(inputChord.notes)
        del inputChord
        
        #show the note of the chord
        #inputMode=new Mode(inputRoot,)