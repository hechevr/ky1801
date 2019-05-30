import os
import sys
import numpy as np

from model import Model
from model import generate_train_dataset

from preprocessing.preprocessing import PreProcessing
from config import config

def keychange(barnum):
    print("Key change at bar %d" % barnum)
    return sys.argv[1]

# main function for system
def main(filepath, pp):
    # load every score in following folder for training
    train_data_dir = config.data_dir
    train_list = [os.path.join(train_data_dir, f) for f in os.listdir(train_data_dir)]
    # initialize lstm model
    lstm = Model()
    # pretrain using fake data
    lstm.pretrain(iteration=config.pretrain_step)
    # train the model with real data
    lstm.train(train_list, config.training_step)

    # evaluating system
    predict = []
    score_list = []
    label_list = []
    max_iteration = 8
    limited = 0.5
    changekey = -1
    for i in range(max_iteration):
        pos, test_x = generate_train_dataset(filepath, return_pos=True, test=True)
        # pos, test_x, test_y = generate_train_dataset(sys.argv[2], return_pos=True)
        label, likelihood = lstm.predict(test_x)
        print(likelihood)

        score = np.mean(likelihood)
        print('score', score)
        # output the label
        threshold = 0.80
        if (score > threshold):
            # if score is small, return the predict
            predict = label
            break
        else:
            # if score is large, key change
            score_list.append(score)
            label_list.append(label)
            # find the possible possition that result in bad likelihood
            for j in range(len(label)):
                if (likelihood[j] < limited):
                    barnum = int(pos[j+1])
                    if changekey < barnum:
                        changekey = barnum
                        break
            # pass barnum to preprocessing
            print("key change to %d"%barnum)
            pp.KeyCheck(barnum)
            pp.DataUpdate()
            pp.WriteToFileData("./")
            pp.WriteToFileKey("./")

    if (len(predict) > 0):
        print("predict: ")
        label = [lstm.vec2chord(v) for v in predict]
        label_idx = predict
        label_list.append(predict)
    else:
        # find the predict with highest score
        idx = np.argmax(score_list)
        idx = len(score_list) - 1
        print(score_list)
        print(idx)
        label = [lstm.vec2chord(v) for v in label_list[idx]]
        label_idx = label_list[idx]

    # write output to csv file
    label = [lstm.vec2chord(v) for v in label_list[idx]]
    fo = open(config.output_file, "w")
    for i in range(len(label)):
        fo.write(pos[i])
        fo.write(",")
        fo.write(label[i])
        fo.write("\n")    



    """
    for idx in range(len(score_list)):
        label = [lstm.vec2chord(v) for v in label_list[idx]]
        p, d, l = generate_train_dataset(sys.argv[2], return_pos=True)
        p = p[1:]
        d = d[1:]
        l = l[1:]
        print(len(l), len(label))
        ll = [lstm.vec2chord(v) for v in np.argmax(l, axis=1)]
        ll_idx = np.argmax(l, axis=1)
        ll_label= [lstm.vec2chord(v) for v in ll_idx]
        correct = 0
        print(label)
        print(ll_label)
        for idx in range(len(ll_label)):
            for i in range(len(label)):
                if (int(pos[i]) == int(p[idx])):
                    if (label[i] == ll_label[idx]):
                        correct += 1
                        break
        accuracy = correct / len(ll_label)
        print(accuracy)       
    """





if __name__ == '__main__':

    pp = PreProcessing(sys.argv[1])
    pp.WriteToFileData("./")
    filepath = './data.csv'
    main(filepath, pp)