from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

import numpy as np

import utils

label_template = [v for v in utils.CHORD.keys()]

dimension = 12
timestep = 2

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
        train_x.append(v)
        """
        for i in range(len(vector_list)):
            if ('1' in vector_list[i]):
                v[i] = 1
            elif ('2' in vector_list[i]):
                v[i] = 2
            elif ('3' in vector_list[i]):
                v[i] = 3
        train_x.append(v)
        """


    train_y = []
    for chord in label:
        ch = chord.replace(" ", "")
        l = [0] * len(label_template)
        l[utils.CHORD[ch]] = 1
        train_y.append(l)

    """
    for line in data:
        batch = []
        for vector in line:
            v = [0] * dimension
            vector_list = vector.split(',')
            for i in range(len(vector_list)):
                if ('1' in vector_list[i]):
                    v[i] = 1
                elif ('2' in vector_list[i]):
                    v[i] = 2
                elif ('3' in vector_list[i]):
                    v[i] = 3
            batch.append(v)
        train_x.append(batch)
    """

    """
    train_y = []
    for line in label:
        batch = []
        for chord in line:
            ch = chord.replace(" ", "")
            l = [0] * len(label_template)
            l[utils.CHORD[ch]] = 1
            batch.append(l)
        train_y.append(batch)
    """



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

def lstm_train(data, size=5):
    train_x = []
    for x in range(size, len(data)+1):
        for i in range(size):
            train_x.append(data[x-size+i])
    return train_x

# train_x, train_y = generat_train_dataset('Mozart1_standard_8.csv')
# train_x1, train_y1 = generat_train_dataset('Von_fremden_Lndern_und_Menschen.csv')
# train_x2, train_y2 = generat_train_dataset('the happy farmer.csv')

train_x1, train_y1 = generate_train_dataset("data/Vondata.csv")
train_x2, train_y2 = generate_train_dataset("data/thehfdata.csv")

train_x = train_x1 + train_x2
train_y = train_y1 + train_y2

model = Sequential()
model.add(LSTM(32, input_shape=(timestep, dimension)))
model.add(Dense(len(label_template), activation='softmax'))
model.compile(loss="mean_squared_error", optimizer='adam')

X = lstm_train(train_x, timestep)
Y = train_y

train_n = 20
trX = np.reshape(X[:-train_n*timestep], (int(len(X[:-train_n*timestep])/timestep), timestep, dimension))
trY = np.reshape(Y[timestep-1:-train_n], (len(Y[timestep-1:-train_n]), len(label_template)))
print(len(X))
print(len(train_y))
print(trX.shape)
print(trY.shape)

model.fit(trX, trY, epochs=50, batch_size=1, verbose=2)

"""
for epoch in range(2):
    for index in range(1, len(train_x)):
        # input shape = [batch_size, timestep, input_dim]
        size = len(train_x[index])
        tx = np.reshape(train_x[index], (size, 1, dimension))
        ty = np.reshape(train_y[index], (size, len(label_template)))
        model.fit(tx, ty, epochs=100, batch_size=1, verbose=10)
teX = train_x[0]
teY = train_y[0]
teX = np.reshape(teX, (len(teX), 1, dimension))
teY = np.reshape(teY, (len(teY), len(label_template)))
train_predict = model.predict(teX)
print(train_predict)
print(teY)
"""

test_n = 20
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

