import csv
import sys

major = ['C', 'C#', 'Cb', 'D', 'D#', 'Db', 'E', 'E#', 'Eb', 'F', 'F#', 'Fb', 'G', 'G#', 'Gb', 'A', 'A#', 'Ab', 'B', 'B#', 'Bb', 'c', 'c#', 'cb', 'd', 'd#', 'db', 'e', 'e#', 'eb', 'f', 'f#', 'fb', 'g', 'g#','gb','a','a#','ab','b', 'b#', 'bb']

# s = [chord keys]
def parser(s):
    if (len(s) < 1):
        return []
    vec = [0] * 7
    vec_str = s.split()
    print(vec_str)
    if ('C' in vec_str):
        vec[0] = 1
    if ('D' in vec_str):
        vec[1] = 1
    if ('E' in vec_str):
        vec[2] = 1
    if ('F' in vec_str):
        vec[3] = 1
    if ('G' in vec_str):
        vec[4] = 1
    if ('A' in vec_str):
        vec[5] = 1
    if ('B' in vec_str):
        vec[6] = 1
    return vec
	
def load_table():
    table = []
    with open("output.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (row[0] in major):
                title = row[0]
            else:
                row[0] = title + " " + row[0]
                table.append(row)
    return table

def lookup(s, table):
    data = []
    for t in table:
        # print(s, t)
        if s in t:
            data.append(t)
    return data

def lookupA(s):
    table = load_table()
    if (s[-1] == '+'):
        stmp = s[0:-1]
    else:
        stmp = s
    res = lookup(stmp, table)
    if (len(res[0][1]) == 0 or len(res[0][2]) == 0):
        return res[0][1]
    elif ('+' in s):
        return res[0][2]
    else:
        return res[0][1]

def lookup_vec(s):
    table = load_table()
    if (s[-1] == '+'):
        stmp = s[0:-1]
    else:
        stmp = s
    res = lookup(stmp, table)
    if (len(res[0][1]) == 0 or len(res[0][2]) == 0):
        return parser(res[0][1])
    elif ('+' in s):
        return parser(res[0][2])
    else:
        return parser(res[0][1])
		
if __name__ == "__main__":
    table = load_table()
    # print(table)
    print(lookup(sys.argv[1], table))
