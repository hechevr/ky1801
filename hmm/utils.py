import numpy as np
import pickle

CHORD = {
    'I': 0,
    'I+': 1,
    'II': 2,
    'II+': 2,
    'III': 3,
    'III+': 4,
    'IV': 5,
    'IV+': 6,
    'V': 7,
    'V+': 8,
    'bVI': 9,
    'VI': 10,
    'VI+': 11,
    'GVI': 12,
    'FVI': 13,
    'ItVI': 14,
    'VII': 15,
    'VII+': 16,
    'DVII': 17,
    'Nah': 18
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