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
    with open(test_file, "r") as fo:
        reader = csv.reader(fo)
        d = []
        l = []
        for row in reader:
            # print(row)
            if (len(row[2]) > 0):
                d.append(row[1])
                l.append(row[2])
            else:
                data.append(d)
                label.append(l)
                d = []
                l = []

    return data, label
