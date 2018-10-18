import sys
import re
from enum import Enum

def FindRoot(input):
    global chordRoot
    for root in Root:
        if (input==root.name):
            chordRoot=root 
            break
    
class Root(Enum):
    C='C'
    Db='Db'
    D='D'
    Eb='Eb'
    E='E'
    F='F'
    Gb='Gb'
    G='G'
    Ab='Ab'
    A='A'
    Bb='Bb'
    B='B'


class ChordNum(Enum):
    triad=3
    seventhChord=4
    ninthChord=5
    eleventhChord=6
    thirteenthChord=7

class ChordType(Enum):
    Major='maj'
    Minor='m'
    Dominant=''
    Aug='aug'
    Dim='dim'
    Sus='sus'
    Null='no'
def main():
    majorThird=4
    minorThird=3
    majorSecond=2
    majorChordTable={1:majorThird,2:minorThird,3:majorThird,4:minorThird,5:minorThird,6:majorThird}
    minorChordTable={1:minorThird,2:majorThird,3:minorThird,4:majorThird,5:minorThird,6:majorThird}
    dominantCHordTable={1:majorThird,2:minorThird,3:minorThird,4:majorThird,5:minorThird,6:majorThird}
    noteTable={1:Root.C,2:Root.Db,3:Root.D,4:Root.Eb,5:Root.E,6:Root.F,7:Root.Gb,8:Root.G,9:Root.Ab,10:Root.A,11:Root.Bb,12:Root.B}
    augChordTable={1:majorThird,2:majorThird,3:majorSecond}
    print('press b to begin to id chord')
    if(input()!='b'):
        print('end id')
    else:
        print('input quit to quit')
        while(input()!='quit'):
            #input root
            chordRoot=Root.C
            print('input the root of your chord')
            inputRoot=input()
            FindRoot(inputRoot)
           
            #get next root
            chordNotes=[chordRoot]
            
            #input discription
            print('input your chord discription')
            chordDis=input()
            if(chordDis==''):
                # major 3
               chordNum=ChordNum.triad
               chordType=ChordType.Major
            elif(chordDis=='m'):
                chordNum=ChordNum.triad
                chordType=ChordType.Minor
            elif(chordDis=='aug'):
                chordNum=ChordNum.triad
                chordType=ChordType.Aug
            elif(chordDis=='dim'):
                chordNum=ChordNum.triad
                chordType=ChordType.Dim
            elif(chordDis=='sus4' or chordDis=='sus2'):
                number=re.findall(r'\d+',chordDis)
                chordNum=ChordNum.triad
                chordType=ChordType.Sus
            else:
                #print('first',chordDis)
                number=re.findall(r'\d+',chordDis)
                #print('number 0',number[0])
                number0=int(number[0])
                if(number0==7):
                    chordNum=ChordNum.seventhChord
                elif(number0==9):
                    chordNum=ChordNum.ninthChord
                elif(number0==11):
                    chordNum=ChordNum.eleventhChord
                elif(number0==13):
                    chordNum=ChordNum.thirteenthChord
                #print(chordDis)
                splitDis=chordDis.split(number[0])   
                #print(splitDis)
                type=splitDis[0]
                if(len(number)==2):
                    splitDis1=splitDis[1].split(number[1])
                    #print('split',splitDis1)
                    type=splitDis1[0]
                #print('type',type)
                if(type=='maj'):
                    chordType=ChordType.Major
                elif(type=='m'):
                    chordType=ChordType.Minor
                elif(type=='aug'):
                    chordType=ChordType.Aug
                elif(type=='dim'):
                    chordType=ChordType.Dim
                elif(type==''):
                    chordType=ChordType.Dominant
                elif(type=='sus'):
                    chordType=ChordType.Sus
                else:
                    chordType=ChordType.Null
                #print('chord type ',chordType)
                #print('chord num ',chordNum)
            
            firstNote=chordRoot
            secondNote=chordRoot
            #print("value",chordNum.value)
            for i in range (chordNum.value-1):
                for index,note in noteTable.items():
                    if(note==firstNote):
                        firstIndex=index
                if(chordType==ChordType.Major):    
                    secondIndex=firstIndex+majorChordTable[i+1]
                if(chordType==ChordType.Minor):
                    secondIndex=firstIndex+minorChordTable[i+1]
                if(chordType==ChordType.Dominant or chordType==ChordType.Sus):
                    secondIndex=firstIndex+dominantCHordTable[i+1]
                if(chordType==ChordType.Dim):
                    secondIndex=firstIndex+3
                if(chordType==ChordType.Aug):
                    secondIndex=firstIndex+augChordTable[i+1]
                if(secondIndex>12):
                    secondIndex=secondIndex-12
                secondNote=noteTable[secondIndex]
                chordNotes.append(secondNote)
                firstNote=secondNote
            if(chordType==ChordType.Sus):
               if(len(number)==1):
                   number1=int(number[0])
               elif(len(number)==2):
                   number1=int(number[1])
               for index, note in noteTable.items():
                   if(note==chordNotes[1]):
                       susIndex=index
               if(number1==4):
                   susNote=noteTable[susIndex+1]
               elif(number1==2):
                   susNote=noteTable[susIndex-2]
               chordNotes[1]=susNote
            print(chordNotes)
            print('quit to quit')

def chord_id(r, d):
    majorThird=4
    minorThird=3
    majorSecond=2
    majorChordTable={1:majorThird,2:minorThird,3:majorThird,4:minorThird,5:minorThird,6:majorThird}
    minorChordTable={1:minorThird,2:majorThird,3:minorThird,4:majorThird,5:minorThird,6:majorThird}
    dominantCHordTable={1:majorThird,2:minorThird,3:minorThird,4:majorThird,5:minorThird,6:majorThird}
    noteTable={1:Root.C,2:Root.Db,3:Root.D,4:Root.Eb,5:Root.E,6:Root.F,7:Root.Gb,8:Root.G,9:Root.Ab,10:Root.A,11:Root.Bb,12:Root.B}
    augChordTable={1:majorThird,2:majorThird,3:majorSecond}

    #input root
    chordRoot=Root.C
    inputRoot=r
    FindRoot(inputRoot)
    
    #get next root
    chordNotes=[chordRoot]
    
    #input discription
    chordDis = d
    if(chordDis==''):
        # major 3
       chordNum=ChordNum.triad
       chordType=ChordType.Major
    elif(chordDis=='m'):
        chordNum=ChordNum.triad
        chordType=ChordType.Minor
    elif(chordDis=='aug'):
        chordNum=ChordNum.triad
        chordType=ChordType.Aug
    elif(chordDis=='dim'):
        chordNum=ChordNum.triad
        chordType=ChordType.Dim
    elif(chordDis=='sus4' or chordDis=='sus2'):
        number=re.findall(r'\d+',chordDis)
        chordNum=ChordNum.triad
        chordType=ChordType.Sus
    else:
        #print('first',chordDis)
        number=re.findall(r'\d+',chordDis)
        #print('number 0',number[0])
        number0=int(number[0])
        if(number0==7):
            chordNum=ChordNum.seventhChord
        elif(number0==9):
            chordNum=ChordNum.ninthChord
        elif(number0==11):
            chordNum=ChordNum.eleventhChord
        elif(number0==13):
            chordNum=ChordNum.thirteenthChord
        #print(chordDis)
        splitDis=chordDis.split(number[0])   
        #print(splitDis)
        type=splitDis[0]
        if(len(number)==2):
            splitDis1=splitDis[1].split(number[1])
            #print('split',splitDis1)
            type=splitDis1[0]
        #print('type',type)
        if(type=='maj'):
            chordType=ChordType.Major
        elif(type=='m'):
            chordType=ChordType.Minor
        elif(type=='aug'):
            chordType=ChordType.Aug
        elif(type=='dim'):
            chordType=ChordType.Dim
        elif(type==''):
            chordType=ChordType.Dominant
        elif(type=='sus'):
            chordType=ChordType.Sus
        else:
            chordType=ChordType.Null
        #print('chord type ',chordType)
        #print('chord num ',chordNum)
    
    firstNote=chordRoot
    secondNote=chordRoot
    #print("value",chordNum.value)
    for i in range (chordNum.value-1):
        for index,note in noteTable.items():
            if(note==firstNote):
                firstIndex=index
        if(chordType==ChordType.Major):    
            secondIndex=firstIndex+majorChordTable[i+1]
        if(chordType==ChordType.Minor):
            secondIndex=firstIndex+minorChordTable[i+1]
        if(chordType==ChordType.Dominant or chordType==ChordType.Sus):
            secondIndex=firstIndex+dominantCHordTable[i+1]
        if(chordType==ChordType.Dim):
            secondIndex=firstIndex+3
        if(chordType==ChordType.Aug):
            secondIndex=firstIndex+augChordTable[i+1]
        if(secondIndex>12):
            secondIndex=secondIndex-12
        secondNote=noteTable[secondIndex]
        chordNotes.append(secondNote)
        firstNote=secondNote
    if(chordType==ChordType.Sus):
       if(len(number)==1):
           number1=int(number[0])
       elif(len(number)==2):
           number1=int(number[1])
       for index, note in noteTable.items():
           if(note==chordNotes[1]):
               susIndex=index
       if(number1==4):
           susNote=noteTable[susIndex+1]
       elif(number1==2):
           susNote=noteTable[susIndex-2]
       chordNotes[1]=susNote
    # print(chordNotes)
    # print('quit to quit')
    return chordNotes

# main()
