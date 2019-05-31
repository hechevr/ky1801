from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras

import numpy as np

import utils

import matplotlib.pyplot as plt

label_template = [v for v in utils.CHORD.keys()]

dimension = 12
timestep = 2

# convert string into vector
def parser(data, label):
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
        l = [0] * len(label_template)
        l[utils.CHORD[ch]] = 1
        train_y.append(l)

    for i in range(len(data)):
        print(train_x[i])

    print(utils.CHORD)
    for i in range(len(label)):
        print(train_y[i])
        print(label[i])



    return train_x, train_y


# generate train x and layer
def generate_train_dataset(datapath):
    pos, data, label = utils.load_data_new(datapath)

    train_x, train_y = parser(data, label)

    return train_x, train_y

# convert data into LSTM format
def lstm_train(data, size=5):
    train_x = []
    for x in range(size, len(data)+1):
        for i in range(size):
            train_x.append(data[x-size+i])
    return train_x

# load pretrain data
pretrain_x, pretrain_y = generate_train_dataset('pretrain_data.csv')


# create LSTM model
model = Sequential()
model.add(LSTM(32, input_shape=(timestep, dimension)))
model.add(Dense(len(label_template), activation='softmax'))
model.compile(loss="mean_squared_error", optimizer='adam')

# feed fake data into model
X = lstm_train(pretrain_x, timestep)
Y = pretrain_y
X = np.reshape(X, (int(len(X)/timestep), timestep, dimension))
Y = np.reshape(Y[1:], (len(Y[1:]), len(label_template)))
pretrain_loss = []
history = model.fit(X, Y, epochs=20, batch_size=1, verbose=2)
pretrain_loss = history.history["loss"]
# print(pretrain_loss)
pretrain_y = [i for i in range(1, 21)]
# plt.plot(pretrain_y, pretrain_loss, label="pretrain")
# plt.savefig('pretrain_loss.png')

# load training data
train_x1, train_y1 = generate_train_dataset("data/Vondata.csv")
train_x2, train_y2 = generate_train_dataset("data/thehfdata.csv")
train_x3, train_y3 = generate_train_dataset("data/Mozart3data.csv")
train_x4, train_y4 = generate_train_dataset("data/Mozart5dataG.csv")

train_x = train_x2 + train_x1 + train_x3 +train_x4
train_y = train_y2 + train_y1 + train_y3 + train_y4

X = lstm_train(train_x, timestep)
Y = train_y

train_n = 11
trX = np.reshape(X[:-train_n*timestep], (int(len(X[:-train_n*timestep])/timestep), timestep, dimension))
trY = np.reshape(Y[timestep-1:-train_n], (len(Y[timestep-1:-train_n]), len(label_template)))

it = 30
# training model
history = model.fit(trX, trY, epochs=it, batch_size=1, verbose=2)
pretrain_loss += history.history["loss"]
print(pretrain_loss)
pretrain_y = [i for i in range(1, 1 + len(pretrain_loss))]
# draw loss image
plt.plot(pretrain_y, pretrain_loss, label="train with pretrain")
plt.legend(loc='upper left')
plt.xlabel('Iterations')
plt.ylabel('L2 Loss')
plt.savefig('train_loss.png')

test_n = train_n
teX = X[-timestep*test_n:]
teY = Y[-test_n:]
teX = np.reshape(teX, (-timestep*test_n, timestep, dimension))
teY = np.reshape(teY, (test_n, len(label_template)))
train_predict = model.predict(teX)

print(teX)
print(train_predict)
print(teY)

lr = np.argmax(train_predict, 1)
ll = np.argmax(teY, 1)
lr_likelihood = []
for idx, l in enumerate(lr):
    print(lr[idx])
    lr_likelihood.append(train_predict[idx][l])

print(lr_likelihood)

print(lr)
print(ll)

res = np.mean(np.equal(lr, ll))
print('acc: ', res)

# output
chord_list = utils.CHORD_INV
out_label = [chord_list[v] for v in ll]
out_predict = [chord_list[v] for v in lr]
out_input = train_x[-test_n:]
fo = open("output.csv", "w")
fo.write("input;label;predict;likelihood\n")
for idx in range(len(out_input)):
    line = str(out_input[idx]) + ";" + str(out_label[idx]) + ";" + str(out_predict[idx]) + ";" + str(lr_likelihood[idx]) + "\n" 
    fo.write(line)
fo.close()

