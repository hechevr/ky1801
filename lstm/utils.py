import numpy as np
import pickle
import csv

CHORD = {
    'I': 0,
    'I+': 1,
    'II': 2,
    'II+': 3,
    'III': 4,
    'III+': 5,
    'IV': 6,
    'IV+': 7,
    'V': 8,
    'V+': 9,
    'VI': 10,
    'VI+': 11,
    'VII': 12,
    'VII+': 13,
    'Nah': 14
}
CHORD_INV = {
    0: 'I',
    1: 'I+',
    2: 'II',
    3: 'II+',
    4: 'III',
    5: 'III+',
    6: 'IV',
    7: 'IV+',
    8: 'V',
    9: 'V+',
    10: 'VI',
    11: 'VI+',
    12: 'VII',
    13: 'VII+',
    14: 'Nah'
}

def chordidx(s):
    if '+' in s:
        return int((CHORD[s]-1)/2)
    else:
        return int(CHORD[s]/2)

def load_obj(name):
    with open('Scores/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_train_files():
    train_file = open("Scores/train_file.txt", "r")
    filelist = []
    for line in train_file:
        line = line.rstrip()
        filelist.append(line)
    train_file.close()

    data = []
    for f in filelist:
        data.append(load_obj(f))
        print("Train file " + f + " has been loaded")
    print("\n")
    return np.array(preprocess(data))

def preprocess(data):
    newdata = []
    for page in data:
        for line in page:
            newdata.append([line[0], line[1]])
    print(newdata)
    return newdata

"""
only load observation sequence
"""
def load_train_data(train_file):
    data = []
    with open(train_file, "r") as fo:
        reader = csv.reader(fo)
        for row in reader:
            data.append(row[1])
    return data

"""
load observation sequence and chord
"""
def load_test_data(test_file):
    data = []
    with open(test_file, "r") as fo:
        reader = csv.reader(fo)
        for row in reader:
            if (len(row[2]) > 0):
                data.append([row[1], row[2]])
    return data

def load_data(test_file):
    data = []
    label = []
    pos = []
    with open(test_file, "r", encoding="utf-8-sig") as fo:
        reader = csv.reader(fo)
        d = []
        l = []
        p = []
        for row in reader:
            # print(row)

            if (row[2] == 'X' or len(row[2]) == 0):
                label.append('Nah')
            else:
                label.append(row[2].replace("7", "+"))

            data.append(row[1])
            # l.append(row[2].replace("7", "+"))
            pos.append(row[0])
            """
            if (row[2] == 'X' or len(row[2]) == 0 or len(row[3]) != 0):

                if (len(d) > 0):
                    data.append(d)
                    label.append(l)
                    pos.append(p)
                    d = []
                    l = []
                    p = []

            else:
                d.append(row[1])
                l.append(row[2].replace("7", "+"))
                p.append(row[0])
            """


    return pos, data, label

def load_data_new(test_file):
    data = []
    label = []
    pos = []
    with open(test_file, "r", encoding="utf-8-sig") as fo:
        reader = csv.reader(fo, delimiter=";")
        for row in reader:
            if (row[0] == ""):
                continue
            if (row[0][0] == "."):
                continue
            # parser vector
            vec_str = row[1]
            vec_str = vec_str.replace(" ", "")
            vec_str = vec_str.replace("[[", ",")
            vec_str = vec_str.replace("[", "")
            vec_str = vec_str.replace("]]", "")
            vec = vec_str.split("]")

            print(vec)
            for idx, v in enumerate(vec):
                numvec = v
                data.append(numvec[1:])
                pos.append(row[0])
                if (idx + 2 < len(row)):
                    label.append(row[idx + 2])
                else:
                    label.append("Nah")

    print(len(pos))
    print(len(data))
    print(len(label))
    """
    for idx, d in enumerate(pos):
        print(pos[idx], data[idx], label[idx])    
    """


    return pos, data, label

def read_trans_prob(filename):
    prob = []
    with open(filename, "r") as fo:
        reader = csv.reader(fo)
        for idx, row in enumerate(reader):
            if (idx > 0):
                prob.append(row[1:])
    print(prob)
    return prob
