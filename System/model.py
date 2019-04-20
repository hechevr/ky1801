from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras

import numpy as np

import utils

# parse label from string to vector
def parser(data, label, dimension=12, labeldimentsion=15):
    # convert data into vector
    train_x = []
    for vector in data:
        v = [0] * dimension
        vector_list = vector.split(',')
        # parser float vector
        for i in range(len(vector_list)):
            s = vector_list[i]
            s = s.replace("[", "")
            s = s.replace("]", "")
            s = s.replace(" ", "")
            # print(s)
            v[i] = float(s)
            if v[i] > 0:
                v[i] = v[i]
        train_x.append(v)

    train_y = []
    for chord in label:
        ch = chord.replace(" ", "")
        l = [0] * labeldimentsion
        l[utils.CHORD[ch]] = 1
        train_y.append(l)

    return train_x, train_y

# parse label from string to vector
def parser_x(data, dimension=12, labeldimentsion=15):
    # convert data into vector
    train_x = []
    for vector in data:
        v = [0] * dimension
        vector_list = vector.split(',')
        # parser float vector
        for i in range(len(vector_list)):
            s = vector_list[i]
            s = s.replace("[", "")
            s = s.replace("]", "")
            s = s.replace(" ", "")
            # print(s)
            v[i] = float(s)
            if v[i] > 0:
                v[i] = v[i]
        train_x.append(v)
    return train_x

# generate train x and layer
def generate_train_dataset(datapath, return_pos=False, test=False):
    if (test):
        pos, data = utils.load_test_data(datapath)
        train_x = parser_x(data)
        if (not return_pos):
            return train_x
        else:
            return pos, train_x
    else:
        pos, data, label = utils.load_data_new(datapath)
        train_x, train_y = parser(data, label)
        if (not return_pos):
            return train_x, train_y
        else:
            return pos, train_x, train_y



# generate X in lstm format
def lstm_train(data, size=5):
    train_x = []
    for x in range(size, len(data)+1):
        for i in range(size):
            train_x.append(data[x-size+i])
    return train_x

# lstm model
class Model(object):
    def __init__(self, timestep=2, dimension=12, labeldimension=15):
        self.timestep = timestep
        self.dimension = dimension
        self.labeldimension = labeldimension
        self.model = Sequential()
        self.model.add(LSTM(32, input_shape=(self.timestep, self.dimension)))
        self.model.add(Dense(labeldimension, activation='softmax'))
        self.model.compile(loss="mean_squared_error", optimizer='adam')

    # feed model with fake data
    def pretrain(self, pretrain_path='pretrain_data.csv', iteration=20):
        pretrain_x, pretrain_y = generate_train_dataset(pretrain_path)
        X = lstm_train(pretrain_x, self.timestep)
        X = np.reshape(X, (int(len(X)/self.timestep), self.timestep, self.dimension))
        Y = pretrain_y
        Y = np.reshape(Y[1:], (len(Y[1:]), self.labeldimension))

        self.model.fit(X, Y, epochs=iteration, verbose=2)
    # train the model with real data
    def train(self, datadir, iteration=50):
        train_x = []
        train_y = []
        for path in datadir:
            x, y = generate_train_dataset(path)
            train_x = train_x + x
            train_y = train_y + y
        X = lstm_train(train_x, self.timestep)
        Y = train_y
        X = np.reshape(X, (int(len(X)/self.timestep), self.timestep, self.dimension))
        Y = np.reshape(Y[1:], (len(Y[1:]), self.labeldimension))

        self.model.fit(X, Y, epochs=iteration, verbose=2)
    # predict the result for test_x
    def predict(self, test_x):
        X = lstm_train(test_x, self.timestep)
        X = np.reshape(X, (int(len(X)/self.timestep), self.timestep, self.dimension))
        output = self.model.predict(X)
        label = np.argmax(output, 1)
        likelihood = []
        for idx, l in enumerate(label):
            likelihood.append(output[idx][l])

        self._score = np.mean(likelihood)

        return label, likelihood
    # evaluate the model: return accuracy
    def evaluate(self, test_x, test_y):
        X = lstm_train(test_x, self.timestep)
        X = np.reshape(X, (int(len(X) / self.timestep), self.timestep, self.dimension))
        Y = test_y
        Y = np.reshape(Y[1:], (len(Y[1:]), self.labeldimension))
        output = self.model.predict(X)
        predict_label = np.argmax(output, 1)
        Y_label = np.argmax(Y, 1)
        likelihood = []
        for idx, l in enumerate(predict_label):
            likelihood.append(output[idx][l])

        res = np.mean(np.equal(Y_label, predict_label))
        return res

    def score(self):
        return self._score
    def vec2chord(self, num):
        return utils.CHORD_INV[num]
