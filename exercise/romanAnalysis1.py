'''
Purpose:
        Given several notes, return the correct chord
        using ROman numeral to express the chored
22/10/2018: Add # and flat key of chord, NoteShift, IntCheck, minorModeTable need to change
23/10/2018  NoteOfChord function unfinished. 
            NoteSHift only calcute flat notes
            NoteInRoman return flat notes of the give notes
            Correct express is still unfinished.
24/10/2018: debuging the correct notes. the other type need to change.sChordType
25/10/2018  finish other parts and get result except minor foat chord
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
    sIndex=noteTable[note]
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
    return rNote
   

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
    #for C# and C flat, return C
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
    #find the calculate note of the chord
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
        mKey=NoteOrigin(mKey)
    tableIndex=flatCheckList.index(mKey)
       # print('table index is ',tableIndex)
    if mType==ModeType.Minor:
        roKey=minorModeTable[tableIndex][roValue]
    elif mType==ModeType.Major:
        roKey=majorModeTable[tableIndex][roValue]
    if isFlat is True:
        roKey=NoteShift(True,roKey)
    elif isSharp is True:
        roKey=NoteShift(False,roKey)
    #find the correct note for expression
    chordIndex=tableIndex+roValue
    if chordIndex>6:
        chordIndex=chordIndex-7

    chordRoot=flatCheckList[chordIndex]
    #roKey correct note
    #chordRoot correct note with wrong express
    return roKey,roValue+1,chordRoot
# find note of aug 6 chord
def FlatToSharp(note):
    if NoteIsFlat(note)==True:
        index=flatList.index(note)
        sIndex=index-1
        if sIndex==-1:
            sIndex=6
        rNote=sharpList[sIndex]
    return rNote
def SharpToFlat(note):
    if NoteIsSharp(note)==True:
        index=sharpList.index(note)
        sIndex=index+1
        if sIndex==7:
            sIndex=0
        rNote=flatList[rNote]    
    return rNote
def InterCheck(i,f,s):
    f=NoteOrigin(f)
    if i==3 or i==4:
        sIndex=flatCheckList.index(f)+2
    if sIndex>6:
        sIndex=sIndex-7
   # print('sIndex is',sIndex)
    oriS=flatCheckList[sIndex]
#    print('s is ',s)
    result=NoteResult(oriS,s)
 #   print('in inter check, result is',result,'origin second note is',oriS)
    return result,oriS

 
def NoteResult(oNote,note):
    interList=[]
    absList=[]
#    print('oNote is',oNote,'note is',note)
    interList.append(wholeNoteTable[note]-wholeNoteTable[oNote])
    absList.append(abs(interList[0]))
    interList.append(wholeNoteTable[note]-wholeNoteTable[oNote]+12)
    absList.append(abs(interList[1]))
    interList.append(wholeNoteTable[note]-wholeNoteTable[oNote]-12)
    absList.append(abs(interList[2]))
    mValue=min(absList)
    mIndex=absList.index(mValue)
 #   print('interList is',interList)
    inter=interList[mIndex]
    result=oNote.value
    #print('inter is',inter)
    if inter>0:
        for i in range(inter):
            result=result+'#'
    elif inter<0:
     #   print('result after plus b',result)
        for i in range(-inter):
            result=result+'b'
    
   # print('result before return',result)
    return result

def Aug6Chord(mKey,type):
    chordNotes=[]
    output=[]
    result=NoteInRoman(ModeType.Major,mKey,'VI')
    firstNote=NoteShift(True,result[0])
    #print('fn',result[2],'sn',firstNote)
    output.append(NoteResult(result[2],firstNote))
    chordNotes.append(firstNote)
    chordNotes.append(mKey)
    output.append(mKey.value)
    if type==SChordType.FA6:
        result=NoteInRoman(ModeType.Major,mKey,'II')
        chordNotes.append(result[0])
        output.append(NoteResult(result[2],result[0]))
    elif type==SChordType.GA6:
        result=NoteInRoman(ModeType.Major,mKey,'III')
        thirdNote=NoteShift(True,result[0])
        output.append(NoteResult(result[2],thirdNote))
        chordNotes.append(thirdNote)
    result=NoteInRoman(ModeType.Major,mKey,'IV')
    lastNote=NoteShift(False,result[0])
    chordNotes.append(lastNote)

    #print('result 2 is ',result[2])
    output.append(NoteResult(result[2],lastNote))

    return chordNotes,output

def GetOutput(output):
    re=''
    for c in output:
        re=re+c+' '
    return re
#find the chord notes
def NotesOfChord(mode,chord,root):
    #Find the first correct notes.
    
    output=[]
    cNotes=[]
    output.append(NoteResult(root,chord.root))
    #print('chord root origin',output,'chord root note is',chord.root)
    cFirstNote=root
    cNotes.append(root)
    firstNote=chord.root
    secondNote=firstNote
    for i in range (chord.num.value-1):
        firstIndex=noteTable[firstNote]
        if(chord.type==ChordType.Major):    
            interval=majorChordTable[i+1].value
            secondIndex=firstIndex+interval
            #print('second index',secondIndex)
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
       # print('befor sharp check')
        result=InterCheck(interval,cFirstNote,secondNote)
        output.append(result[0])
        cSecondNote=result[1]
        cNotes.append(cSecondNote)
        chord.addNotes(secondNote)
        firstNote=secondNote
        cFirstNote=cSecondNote
    if chord.type==ChordType.Minorf5:
        print('minorf5')
        chord.notes[2]=NoteShift(True,chord.notes[2])
        output[2]=NoteResult(cNotes[2],chord.notes[2])

    #check the speial type    
    if chord.sType==None:
        print('no special')
    else:
        if mode.type==ModeType.Major:   
            if chord.sType==SChordType.flat:
                chord.notes[0]=NoteShift(True,chord.notes[0])
                output[0]=NoteResult(cNotes[0],chord.notes[0])
                chord.notes[2]=NoteShift(True,chord.notes[2])
                output[2]=NoteResult(cNotes[2],chord.notes[2])
            elif chord.sType==SChordType.D:
                chord.notes[3]=NoteShift(True,chord.notes[3])
                output[3]=NoteResult(cNotes[3],chord.notes[3])
        elif mode.type==ModeType.Minor:
            if chord.sType==SChordType.flat:
                chord.notes[0]=NoteShift(True,chord.notes[0])
                output[0]=NoteResult(cNotes[0],chord.notes[0])
            if chord.sType==SChordType.plus:
                chord.notes[1]=NoteShift(False,chord.notes[1])
                output[1]=NoteResult(cNotes[1],chord.notes[1])
            if chord.sType==SChordType.D:
                chord.notes[0]=NoteShift(False,chord.notes[0])
                output[0]=NoteResult(cNotes[0],chord.notes[0])
        outputString=GetOutput(output)
        if chord.sType==SChordType.GA6 or chord.sType==SChordType.FA6 or chord.sType==SChordType.IA6:
            result= Aug6Chord(mode.root,chord.sType) 
            chord.notes=result[0]
            output=result[1]
    outputString=GetOutput(output)
    print('chord notes are ',chord.notes)
    print('output is ',output)
    
    return output

def NoteInRomanCheck():
    mType=ModeType.Major
    for note,index in wholeNoteTable.items():
        print('chord note is ',note)
        for roman in R_N_table:
            print('chord roman is ',roman)
            chord,num,cChord=NoteInRoman(mType,note,roman)
            print('chord root is ',chord)
            print('chord origin is ',cChord)
        print('\n')
def ChordToNotesCheck():
    #inputModeList=['C#','D#','E#','F#','G#','A#','B#']
    inputModeList=['C','cb']
    #inputDisList=['I','II','III','IV','V','VI','VII']
    inputDisList=['DVII']
    #inputDisList=['I+','bII','IV+','V+','GVI','FVI','ItVI']

    for inputMode in inputModeList:
        print('input mode is',inputMode)
        for inputDis in inputDisList:
            print('input dis is',inputDis)
            inputNum='2'
            output=ChordToNote(inputMode,inputDis,inputNum)
            #print('output is ',output)

def ChordToNote(mRoot,dis,num):
    if(mRoot[0]==mRoot[0].lower()):
        modeType=ModeType.Minor
        mRoot=mRoot.upper()
    elif(mRoot[0]==mRoot[0].upper()):
        modeType=ModeType.Major
    if(len(mRoot)>1):
        if mRoot[1]=='B':
            mRoot=mRoot[0]+'b'
        print('mode root is',mRoot)
    for note in Note:
        if note.value==mRoot:
            modeRoot=note
    
    #print(modeRoot)
    inputMode=Mode(modeRoot,modeType)
    #print('inputMode mode root is',modeRoot,'input mode mode type is ',modeType)
    if dis[-1]=='+':
        inputSType=SChordType.plus
        dis=dis[:-1]
        #print('in plus')
        
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

    chordRoot,inputRoman,cChordRoot=NoteInRoman(modeType,modeRoot,dis)
   # print('chord root is ',chordRoot)
    #print("input ROman is ",inputRoman)
    #print('cChordRoot is ',cChordRoot)
    if num=='1':
        if(inputMode.type==ModeType.Major):
            #print('input mode type is major')
            chordType=MajModeTtable[inputRoman]
            inputChord= Chord(chordRoot, ChordNum.triad,chordType,inputSType)
            inputChord.notes = [chordRoot]
            #print('inputchord ',inputChord.notes)
        elif(inputMode.type==ModeType.Minor):
           # print('input mode type is minor')
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
    
    output=''
          
    #print('input chord type is ',inputChord.type)
    output=NotesOfChord(inputMode,inputChord,cChordRoot)
    '''
    # result=[]
    result = ""
    for note in returnNotes:
        # result.append(note.value)
        result += note.value
        result += " "
    return result
    '''
    return output
# chord table
majorModeTable=[[Note.C,Note.D,Note.E,Note.F,Note.G,Note.A,Note.B],              
               [Note.D,Note.E,Note.G_f,Note.G,Note.A,Note.B,Note.D_f],      
               [Note.E,Note.G_f,Note.A_f,Note.A,Note.B,Note.D_f,Note.E_f],
               [Note.F,Note.G,Note.A,Note.B_f,Note.C,Note.D,Note.E],             
               [Note.G,Note.A,Note.B,Note.C,Note.D,Note.E,Note.G_f],
               [Note.A,Note.B,Note.D_f,Note.D,Note.E,Note.G_f,Note.A_f],
               [Note.B,Note.D_f,Note.E_f,Note.E,Note.G_f,Note.A_f,Note.B_f]]
minorModeTable=[[Note.C,Note.D,Note.E_f,Note.F,Note.G,Note.A_f,Note.B_f],
                [Note.D,Note.E,Note.F,Note.G,Note.A,Note.B_f,Note.C],
                [Note.E,Note.G_f,Note.G,Note.A,Note.B,Note.C,Note.D],
                [Note.F,Note.G,Note.A_f,Note.B_f,Note.C,Note.D_f,Note.E_f],
                [Note.G,Note.A,Note.B_f,Note.C,Note.D,Note.E_f,Note.F],
                [Note.A,Note.B,Note.C,Note.D,Note.E,Note.F,Note.G],
                [Note.B,Note.D_f,Note.D,Note.E,Note.G_f,Note.G,Note.A]]
augChordTable={1:M_I.M3,2:M_I.M3,3:M_I.M2}
majorChordTable={1:M_I.M3,2:M_I.m3,3:M_I.M3,4:M_I.m3,5:M_I.m3,6:M_I.M3}
minorChordTable={1:M_I.m3,2:M_I.M3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
dominantCHordTable={1:M_I.M3,2:M_I.m3,3:M_I.m3,4:M_I.M3,5:M_I.m3,6:M_I.M3}
noteTable={Note.C:1,Note.D_f:2,Note.D:3,Note.E_f:4,Note.E:5,Note.F:6,Note.G_f:7,Note.G:8,Note.A_f:9,Note.A:10,Note.B_f:11,Note.B:12}   
wholeNoteTable={Note.C_f:12,Note.C:1,Note.C_s:2,Note.D_f:2,Note.D:3,Note.D_s:4,Note.E_f:4,Note.E:5,Note.E_s:6,Note.F_f:5,Note.F:6,Note.F_s:7,Note.G_f:7,Note.G:8,Note.G_s:9,Note.A_f:9,Note.A:10,Note.A_s:11,Note.B_f:11,Note.B:12,Note.B_s:0}   
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
        print('mode')  
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
            #print(outputChord.notes)
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
                   # print('index dif ',indexDif)
                    for musicInterval in M_I:
                        if indexDif==musicInterval.value:
                            outputChord.addInterval(musicInterval)
                            #print('here')
                    firstNote=secondNote
            #print(outputChord.intervals)
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
            ChordToNotesCheck()
           # NoteInRomanCheck()
if __name__ == "__main__":
    main()

