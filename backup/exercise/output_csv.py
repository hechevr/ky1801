import numpy as np
import csv
from chord_lib import chord_id
from romanAnalysis1 import ChordToNote

# root list
root_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
type_list = ['m', '', 'aug', 'dim', 'sus2', 'sus4']

def main():
    # call function to return chord
    table = []
    for i in root_list:
        table.append([i, ''])
        for j in type_list:
            row = [j]
            result = chord_id(i, j)
            row.append(result)
            table.append(row)
    # write chord table to csv file
    with open('output.csv', 'w') as fo:
        writer = csv.writer(fo)
        for row in table:
            writer.writerow(row)

mod_great_list = ["C","C#",'Cb', "D",'D#','Db', "E",'E#','Eb' ,"F",'F#' ,'Fb',"G",'G#','Gb', "A",'A#','Ab', "B",'B#','Bb']
mod_small_list = ["c",'c#','cb', "d",'d#','db' ,"e",'e#','eb' ,"f",'f#','fb', "g",'g#','gb', "a",'a#','ab', "b",'b#','bb']
# mod_great_list = ["C", "D", "E", "F", "G"]
# mod_small_list = ["c", "d"]
small_list = ["I", "I+", "bII", "II", "III", "IV", "IV+", "V", "V+", "VI", "GVI", "FVI", "ItVI", "VII", "DVII"]
great_list = ["I", "II", "III", "IV", "V", "bVI", "VI", "GVI", "FVI", "ItVI", "VII", "DVII"]
three_chord = ["I", "I+", "bII", "II", "III", "IV", "IV+", "V", "V+", "VI", "bVI", "GVI", "FVI", "ItVI", "VII"]
seven_chord = ["I", "II", "III", "IV", "V", "V+", "VI", "VII", "DVII"]

def wtf():
    table = []
    mod_list = mod_great_list + mod_small_list
    for i in mod_list:
        if i in mod_great_list:
            row = [i, "", ""]
            table.append(row)
            for j in great_list:
                print(i, j, "G")
                row = [j]
                if (j in three_chord):
                    try:
                        result = ChordToNote(i, j, "1")
                        string = ""
                        for idx, r in enumerate(result):
                            string += r
                            if (idx < len(result) - 1):
                                string += " "
                        row.append(string)
                    except:
                        row.append("error")
                else:
                    row.append("")
                if (j in seven_chord):
                    try:
                        result = ChordToNote(i, j, "2")
                        string = ""
                        for idx, r in enumerate(result):
                            string += r
                            if (idx < len(result) - 1):
                                string += " "
                        row.append(string)
                    except:
                        row.append("error")
                else:
                    row.append("")
                table.append(row)
        else:
            row = [i, "", ""]
            table.append(row)
            for j in small_list:
                print(i, j)
                row = [j]
                if (j in three_chord):
                    try:
                        result = ChordToNote(i, j, "1")
                        string = ""
                        for idx, r in enumerate(result):
                            string += r
                            if (idx < len(result) - 1):
                                string += " "
                        row.append(string)
                    except:
                        row.append("error")
                else:
                    row.append("")
                if (j in seven_chord):
                    try:
                        result = ChordToNote(i, j, "2")
                        string = ""
                        for idx, r in enumerate(result):
                            string += r
                            if (idx < len(result) - 1):
                                string += " "
                        row.append(string)
                    except:
                        row.append("error")
                else:
                    row.append("")
                table.append(row)
    
    # write chord table to csv file
    with open('output.csv', 'w') as fo:
        writer = csv.writer(fo)
        for row in table:
            writer.writerow(row)


if __name__ == '__main__':
    # main() 
    wtf()
