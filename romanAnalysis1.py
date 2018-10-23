'''
Purpose:
        Given several notes, return the correct chord
        using ROman numeral to express the chored
22/10/2018: Add # and flat key of chord, NoteShift, IntCheck, minorModeTable need to change
23/10/2018 noteInRoman not finished. 
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
    C_f='Cb'
    C='C'
    C_s='C#'
    D_f='Db'
    D='D'
    D_s='D#'
    E_f='Eb'
    E='E'
    E_s="E#"
    F_f="Fb"
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
    B_s='B#'

#music interval class
class M_I(Enum):
    P5=7
    P4=5
    M3=4
    m3=3
    M2=2
    m2=1


class Chord():
    #special is the chord with plus, flat,augment 6 chord
    def __init__(self,root=None,num=None,type=None,sType=None,notes=[],intervals=[]):
        self.root=root
        self.type=type
        self.num=num
        self.notes=notes
        self.sType=sType
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
class SChordType(Enum):
    plus='+'
    flat='b'
    GA6='GA6'
    FA6='FA6'
    IA6='IA6'
    D='Dim'


#functions

def NoteShift(isFlat,note):
    #used in flat table
    sIndex=wholeNoteTable[note]
    if isFlat==True:
        sIndex=sIndex-1
    else:
        sIndex=sIndex+1
    if sIndex>12:
        sIndex=sIndex-12
    elif sIndex<1:
        sIndex=sIndex+12
    for fNote,index in noteTable.items():
        if index==sIndex:
            rNote =fNote
    if isFlat==False:
        rNote=FlatToSharp(rNote)
    return rNote;
   

def NoteIsFlat(note):
    for fNote in flatList:
        if fNote==note:
            return True
    return False
def NoteIsSharp(note):
    for sNote in sharpList:
        if sNote==note:
            return True
    return False
def NoteOrigin(note):
    rNote=note
    for sNote in sharpList:
        if sNote==note:
            index=sharpList.index(sNote)
            rNote=flatCheckList[index]
        
    for fNote in flatList:
        if fNote==note:
            index=flatList.index(fNote)
            rNote=flatCheckList[index]
    return rNote

#given roman back note
def NoteInRoman(mType,mKey,ro):
    isFlat=False
    isSharp=False
    if NoteIsFlat(mKey) is True:
        isFlat=True
    elif NoteIsSharp(mKey) is True:
        isSharp=True
    for roman in R_N_table:
        if roman==ro:
            roValue=R_N_table[roman]-1
    if isFlat is True or isSharp is True:
        omKey=NoteOrigin(mKey)
        tableIndex=flatCheckList.index(omKey)
    else:
        tableIndex=flatCheckList.index(mKey)
        print('table index is ',tableIndex)
    if mType==ModeType.Minor:
        roKey=minorModeTable[tableIndex][roValue]
    elif mType==ModeType.Major:
        roKey=majorModeTable[tableIndex][roValue]
    if isFlat is True:
        roKey=NoteShift(True,roKey)
    elif isSharp is True:
        roKey=NoteShift(False,roKey)
        roKey=NoteShift(True,roKey)
    
    return roKey,roValue+1
# find note of aug 6 chord
def FlatToSharp(note):
    if NoteIsFlat(note)==True:
        for i,j in zip(flatList,sharpList):
            if i==note:
                rNote=j
                break
    return rNote
def SharpToFlat(note):
    if NoteIsSharp(note)==True:
        for i,j in zip(sharpList,flatList):
            if i==note:
                rNote=j
                break
    return rNote
def InterCheck(i,f,s):
    f=NoteOrigin(f)
    if i==3 or i==4:
        sIndex=flatCheckList.index(f)+2
        if sIndex>7:
            sIndex=sIndex-7
        so=flatCheckList[sIndex]
        #if flatCheckTable[f]<flatCheckTable[so]:

        #if cs!=
def SharpCheck(i,f,s):
    #chek the root of the chord
   # i: interval f: first note s:second note
    if NoteIsFlat(s)==False:
        return s
    else:
        f=NoteOrigin(f)
        os=NoteOrigin(s)
        if i==3 or i ==4:
            sIndex=flatCheckTable[f]+2
            if sIndex>7:
                sIndex=sIndex-7
        for note, index in flatCheckTable.items():
            if index==sIndex:
                cs=note
        if cs!=os:
            s=FlatToSharp(s)
    return s        
    #firstNote=root
    for note in chord.notes:
        secondNote=note
        if secondNote==firstNote and NoteIsFlat(note)==False:
            firstNote=secondNote
            continue
        else:
            index=chord.notes.index(secondNote)
            if chord.type==ChordType.Major:
                interval=majorChordTable[index]
               # if interval.value==2 or interval.value==3:

    #if chord.type==ChordType.Major:

def Aug6Chord(mKey,type):
    chordNotes=[]
    firstNote,rIndex=NoteInRoman(ModeType.Major,mKey,'VI')
    if NoteIsFlat(firstNote)==False:
        firstNote=NoteShift(True,firstNote)
    lastNote,rIndex=NoteInRoman(ModeType.Major,mKey,'IV')
    lastNote=NoteShift(False,lastNote)
    chordNotes.append(firstNote)
    chordNotes.append(mKey)
    if type==SChordType.FA6:
        thirdNote,rIndex=NoteInRoman(ModeType.Major,mKey,'II')
        chordNotes.append(thirdNote)
    elif type==SChordType.GA6:
        thirdNote,rIndex=NoteInRoman(ModeType.Major,mKey,'III')
        if NoteIsFlat(thirdNote)==False:
            thirdNote=NoteShift(True,thirdNote)
        chordNotes.append(thirdNote)
    chordNotes.append(lastNote)
    return chordNotes
#find the chord notes
def NotesOfChord(mode,chord):
    cFirstNote=chord.root
    if NoteIsSharp(chord.root)==True:
        #print('true')
        firstNote=SharpToFlat(chord.root)
    else:
        firstNote=chord.root
    secondNote=firstNote
    for i in range (chord.num.value-1):
        firstIndex=noteTable[firstNote]
        if(chord.type==ChordType.Major):    
            interval=majorChordTable[i+1].value
            secondIndex=firstIndex+interval
            print('second index',secondIndex)
        if(chord.type==ChordType.Minor or chord.type==ChordType.Minorf5):
            interval=minorChordTable[i+1].value
            secondIndex=firstIndex+interval
        if(chord.type==ChordType.Dominant):
            interval=dominantCHordTable[i+1].value
            secondIndex=firstIndex+interval
        if(chord.type==ChordType.Dim):
            interval=3
            secondIndex=firstIndex+3
        if(chord.type==ChordType.Aug):
            interval=augChordTable[i+1].value
            secondIndex=firstIndex+augChordTable[i+1].value
        if(secondIndex>12):
            secondIndex=secondIndex-12
        for note in noteTable:
            if noteTable[note]==secondIndex:
                secondNote=note
        print('befor sharp check')
        cSecondNote=SharpCheck(interval,cFirstNote,secondNote)
        chord.addNotes(cSecondNote)
        #print('after add note',chord.notes)
        firstNote=secondNote
        cFirstNote=cSecondNote
        # print("list ",chord.notes)
    # check the minor flat 5  
    if chord.type==ChordType.Minorf5:
        print('minorf5')
        chord.notes[2]=NoteShift(True,chord.notes[2])
        
   
    #check the speial type    
    if chord.sType==None:
        print('no special')
    else:
        if mode.type==ModeType.Major:   
            if chord.sType==SChordType.flat:
                chord.notes[0]=NoteShift(True,chord.notes[0])
                chord.notes[2]=NoteShift(True,chord.notes[2])
            elif chord.sType==SChordType.D:
                chord.notes[3]=NoteShift(True,chord.notes[3])
        elif mode.type==ModeType.Minor:
            if chord.sType==SChordType.flat:
                chord.notes[0]=NoteShift(True,chord.notes[0])
            if chord.sType==SChordType.plus:
                chord.notes[1]=NoteShift(False,chord.notes[1])
            if chord.sType==SChordType.D:
                chord.notes[0]=NoteShift(False,chord.notes[0])
              
        if chord.sType==SChordType.GA6 or chord.sType==SChordType.FA6 or chord.sType==SChordType.IA6:
            chord.notes= Aug6Chord(mode.root,chord.sType) 
        
    print(chord.notes)
    return chord.notes

    
def ChordToNote(mRoot,dis,num):
    if(mRoot[0]==mRoot[0].lower()):
        modeType=ModeType.Minor
        mRoot=mRoot.upper()
    elif(mRoot[0]==mRoot[0].upper()):
        modeType=ModeType.Major
    for note in Note:
        if note.value==mRoot:
            modeRoot=note

    inputMode=Mode(modeRoot,modeType)

    if dis[-1]=='+':
        inputSType=SChordType.plus
        dis=dis[:-1]
        print('in plus')
    elif dis[0]=='b':
        inputSType=SChordType.flat
        dis=dis[1:]
    elif dis[0]=='G':
        inputSType=SChordType.GA6
        dis=dis[1:]
    elif dis[0]=='F':
        inputSType=SChordType.FA6
        dis=dis[1:]
    elif dis[0]=='D':
        inputSType=SChordType.D
        dis=dis[1:]
    elif dis[:2]=='It':
        inputSType=SChordType.IA6
        dis=dis[2:]
    else:
        inputSType=None

    chordRoot,inputRoman=NoteInRoman(modeType,modeRoot,dis)
    if num=='1':
        if(inputMode.type==ModeType.Major):
            chordType=MajModeTtable[inputRoman]
            inputChord= Chord(chordRoot, ChordNum.triad,chordType,inputSType)
            inputChord.notes = [chordRoot]
            #print('inputchord ',inputChord.notes)
        elif(inputMode.type==ModeType.Minor):
            chordType=MinModeTtable[inputRoman]
            inputChord= Chord(chordRoot, ChordNum.triad,chordType,inputSType)
            inputChord.notes = [chordRoot]
    elif num=='2':
        if(inputMode.type==ModeType.Major):
            chordType=MajModeStable[inputRoman]  
            inputChord= Chord(chordRoot,ChordNum.seventhChord,chordType,inputSType)
            inputChord.notes = [chordRoot]
        elif(inputMode.type==ModeType.Minor):
            chordType=MinModeStable[inputRoman]  
            inputChord= Chord(chordRoot,ChordNum.seventhChord,chordType,inputSType)
            inputChord.notes = [chordRoot]
            
    print('input chord type is ',inputChord.type)
    returnNotes=NotesOfChord(inputMode,inputChord)
    # result=[]
    result = ""
    for note in returnNotes:
        # result.append(note.value)
        result += note.value
        result += " "
    return result

# chord table
majorModeTable=[[Note.C,Note.D,Note.E,Note.F,Note.G,Note.A,Note.B],              
               [Note.D,Note.E,Note.F_s,Note.G,Note.A,Note.B,Note.C_s],      
               [Note.E,Note.F_s,Note.G_s,Note.A,Note.B,Note.C_s,Note.D_s],
               [Note.F,Note.G,Note.A,Note.B_f,Note.C,Note.D,Note.E],             
               [Note.G,Note.A,Note.B,Note.C,Note.D,Note.E,Note.F_s],
               [Note.A,Note.B,Note.C_s,Note.D,Note.E,Note.F_s,Note.G_s],
               [Note.B,Note.C_s,Note.D_s,Note.E,Note.F_s,Note.G_s,Note.A_s]]
minorModeTable=[[Note.C,Note.D,Note.E_f,Note.F,Note.G,Note.A_f,Note.B_f],
                [Note.D,Note.E,Note.F,Note.G,Note.A,Note.B_f,Note.C],
                [Note.E,Note.F_s,Note.G,Note.A,Note.B,Note.C,Note.D],
                [Note.F,Note.G,Note.A_f,Note.B_f,Note.C,Note.D_f,Note.E_f],
                [Note.G,Note.A,Note.B_f,Note.C,Note.D,Note.E_f,Note.F],
                [Note.A,Note.B,Note.C,Note.D,Note.E,Note.F,Note.G],
                [Note.B,Note.C_s,Note.D,Note.E,Note.F_s,Note.G,Note.A]]
augChordTable={1:M_I.M3,2:M_I.M3,3:M_I.M2}
majorChordTable={1:M_I.M3,2:M_I.m3,3:M_I.M3,4:M_I.m3,5:M_I.m3,6:M_I.M3}
minorChordTable={1:M_I.m3,2:M_I.M3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
dominantCHordTable={1:M_I.M3,2:M_I.m3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
noteTable={Note.C:1,Note.D_f:2,Note.D:3,Note.E_f:4,Note.E:5,Note.F:6,Note.G_f:7,Note.G:8,Note.A_f:9,Note.A:10,Note.B_f:11,Note.B:12}   
wholeNoteTable={Note.C_f:12,Note.C:1,Note.C_s:2,Note.D_f:2,Note.D:3,Note.D_s:4,Note.E_f:4,Note.E:5,Note.E_s:6,Note.F_f:5,Note.F:6,Note.F_s:7,Note.G_f:7,Note.G:8,Note.G_s:9,Note.A_f:9,Note.A:10,Note.A_s:11,Note.B_f:11,Note.B:12,Note.B_s:1}   
flatCheckTable={Note.C:1,Note.D:2,Note.E:3,Note.F:4,Note.G:5,Note.A:6,Note.B:7} 
flatCheckList=[Note.C,Note.D,Note.E,Note.F,Note.G,Note.A,Note.B]
flatList=[Note.C_f,Note.D_f,Note.E_f,Note.F_f,Note.G_f,Note.A_f,Note.B_f]
sharpList=[Note.C_s,Note.D_s,Note.E_s,Note.F_s,Note.G_s,Note.A_s,Note.B_s]
#roman number table    
R_N_table={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7}
# major mode triad table
MajModeTtable={1:ChordType.Major,2:ChordType.Minor,3:ChordType.Minor,4:ChordType.Major,5:ChordType.Major,6:ChordType.Minor,7:ChordType.Dim}
#major mode seventh table
MajModeStable={1:ChordType.Major,2:ChordType.Minor,3:ChordType.Minor,4:ChordType.Major,5:ChordType.Dominant,6:ChordType.Minor,7:ChordType.Minorf5}
#minor mode triad table
MinModeTtable={1:ChordType.Minor,2:ChordType.Dim,3:ChordType.Major,4:ChordType.Minor,5:ChordType.Minor,6:ChordType.Major,7:ChordType.Major}
#minor mode seventh table
MinModeStable={1:ChordType.Minor,2:ChordType.Minorf5,3:ChordType.Major,4:ChordType.Minor,5:ChordType.Minor,6:ChordType.Major,7:ChordType.Dominant}
def main():
    #main function
    print('input \'quit\' to quit')
    
    
    while input()!='quit':
     
        mode=input('Choose your identification mode\n 1.Note to chord\n 2.Chord to note\n')
    
        while mode!='1' and mode!='2':
            mode=input('Wrong input. Please input the correct answer\n')
    
        if mode=='1':
            inputValue=input('in note to chord mode\n input your notes\n')
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
            '''
            inputMode=input('in chord to note mode\n input your chord Mode\n')
            
            
            inputDis=input('input your chord discription\n')
            
            inputNum=input('Choose your chord mode\n1.triad\n 2.seventh chord\n')
            resultNotes=ChordToNote(inputMode,inputDis,inputNum)
            print(resultNotes)
            #show the note of the chord
            #inputMode=new Mode(inputRoot,)
            '''
            
            for note in Note:
                print
                flatNote=NoteShift(True,inputNote)
                sharpNote=NoteShift(False,inputNote)
            print ('flat note is ',flatNote,'\nsharp note is ',sharpNote)
if __name__ == "__main__":
    main()

