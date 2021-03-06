import numpy as np
from utils import CHORD, load_train_files
import hmmlearn.hmm as hmm_model
from lookup import lookupA
import utils
from sklearn.preprocessing import LabelEncoder

"""
This file is the model for hmm
we only consider C major here
parameter:
    states = [22]
    observations = [2 ^ 7]
    
    hmm:
        start_prob = [22, 1]
        trans_prob = [22, 22]
        emission_prob = [22, 2 ^ 7]
"""

dimension = 8

# hidden markov model class
class hmm(object):
    def __init__(self, n_obs, table):
        self.table = table
        # states = [chord + 'Nah'] = [22]
        self.states = [v for v in CHORD.keys() if 'Nah' not in v]
        self.states.sort()
        self.states.append('Nah')
        self.n_states = len(self.states)

        # observations = [range(0, 128)] = [128]
        self.observations = [int(v) for v in range(n_obs)]
        self.n_obs = n_obs

        # features = vector(observations)
        self.features = [self.obs2vec(v) for v in self.observations]

    def initialize_prob(self, data):
        self.initialize_start_prob(data)
        self.initialize_trans_prob(data)
        self.initialize_emission_prob(data)

    def update_prob(self, data):
        self.update_start_prob(data)
        self.update_trans_prob(data)
        self.update_emission_prob(data)

    def fit(self, data):
        print(len(data))
        td = []
        td_list = []
        for d in data:
            tdt = []
            for s in d:
                tdt.append(code(praservec(s), self.table))
                td_list.append(code(praservec(s), self.table))
            td.append(tdt)
        # create hmm model
        self.hmm = hmm_model.MultinomialHMM(n_components=self.n_states, init_params="", params="s")
        # set model parameters
        self.hmm.startprob_ = np.array(self.start_prob, dtype=np.float64)
        self.hmm.transmat_ = np.array(self.trans_prob, dtype=np.float64)
        self.hmm.emissionprob_ = np.array(self.emission_prob, dtype=np.float64)

        length = [len(l) for l in td]
        itr = 0
        score = -50
        # train model using EM algorithm
        for i in range(0):
            print("score", self.hmm.score(np.reshape(td_list, (-1, 1)), lengths=length))
            self.hmm.fit(np.reshape(td_list, (-1, 1)), lengths=length)
            print("score", self.hmm.score(np.reshape(td_list, (-1, 1)), lengths=length))

        # uncomment this part if not use fit function
        # self.hmm.startprob_ = np.array(self.start_prob, dtype=np.float64)
        # self.hmm.transmat_ = np.array(self.trans_prob, dtype=np.float64)
        # self.hmm.emissionprob_ = np.array(self.emission_prob, dtype=np.float64)

    def predict(self, observations, option='viterbi'):
        print(len(observations))
        print(observations)
        td = []
        for d in observations:
            s = code(praservec(d), self.table)
            td.append(s)
        X = np.reshape(td, (-1, 1))

        # print(X, Xpadding)
        # X = np.concatenate(X, Xpadding)

        return self.hmm.decode(X, algorithm="map")


    # calculate state from observations
    def obs2vec(self, obs):
        vec = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(vec)):
            vec[i] = obs % 2
            obs = int(obs / 2)
        return vec

    # calculate vector from observations
    def vec2obs(self, vec):
        obs = 0
        for i in range(len(vec)):
            obs += 2 ^ i * vec[i]
        return obs

    def initialize_start_prob(self, data):
        # start_prob = start probability
        self.start_prob = np.zeros((self.n_states), dtype=np.float32)
        self.start_prob += 1.0 / self.n_states


    def initialize_trans_prob(self, data):
        # hurestic method by Lucas
        # current implementation: same probability
        # trans_prob = transition probability
        self.trans_prob = np.zeros((self.n_states, self.n_states), dtype=np.float32)
        self.trans_prob += 1.0 / (self.n_states)

    def initialize_emission_prob(self, data):
        print(len(data), self.n_states)
        # emission_prob = emission probability
        self.emission_prob = np.zeros((self.n_states, self.n_obs), dtype=np.float32)
        # self.emission_prob += 1.0 / self.n_obs
        self.emission_prob += 1.0


        # the final state wont be checked
        for i in range(self.n_states - 1):
            for j in range(self.n_obs):
                # print(i, j)
                self.emission_prob[i][j] += similarity(data[i], decode(j, self.table))

        self.emission_prob /= np.sum(self.emission_prob)
        print(self.emission_prob)

    # initialize start_prob
    def update_start_prob(self, data):
        data = np.array(data)
        print(data)
        print(data.shape)
        # chord_list = data[:, 1]
        # chord_list = [c[1:] for c in chord_list]
        chord_list = []
        for d in data:
            for c in d:
                chord_list.append(c)

        for chord in chord_list:
            if (chord in CHORD.keys()):
                self.start_prob[CHORD[chord]] += 1

        # normalize
        self.start_prob = self.start_prob / self.start_prob.sum()
        return self.start_prob

    # initialize transition prob
    def update_trans_prob(self, data):

        """
        for i in range(self.n_states):
            self.trans_prob[i][i] += 3
            self.trans_prob /= np.sum(self.trans_prob, axis=0)


        :param data:
        :return:
        """


        return self.trans_prob

    # initialize emission prob
    def update_emission_prob(self, data):
        """
        for i in range(data.shape[0]):
            if (data[i][1] in CHORD.keys()):
                chord_idx = CHORD[data[i][1]]
                obs_idx = self.vec2obs(data[i][0])
                self.emission_prob[chord_idx][obs_idx] += 1
        # normalize
        # emission_prob = emission_prob / np.sum(emission_prob, axis=0)
        for i in range(self.emission_prob.shape[0]):
            em = self.emission_prob[i]
            s = np.sum(em)
            self.emission_prob[i] /= s
        """

        return self.emission_prob

    def e_trans_prob(self, data):
        for i in range(self.n_states):
            for j in range(self.n_states):

                chord_a = self.states[i]
                chord_b = self.states[j]

                if (chord_a == 'Nah' or chord_b == 'Nah'):
                    continue
                print(chord_a, utils.chordidx(chord_a), chord_b,
                      utils.chordidx(chord_b))

                r = data[utils.chordidx(chord_a)][utils.chordidx(chord_b)]


                if ('H' == r):
                    self.trans_prob[i][j] += 1
                else:
                    self.trans_prob[i][j] += 1

        s = np.sum(self.trans_prob, axis=1)
        s = np.reshape(s, (-1, 1))
        self.trans_prob /= s

    def __str__(self):

        self.start_prob = self.hmm.startprob_
        self.trans_prob = self.hmm.transmat_
        self.emission_prob = self.hmm.emissionprob_
        line = "hmm model for chord identification"
        line += "\nstates:\n"
        line += str(self.states)
        line += "\nobservations:\n"
        line += str(self.observations)
        line += "\nstart_prob:\n"
        line += str(np.array(self.start_prob).shape)
        line += '\n'
        line += str(self.start_prob)
        line += "\ntrans_prob:\n"
        line += str(np.array(self.trans_prob).shape)
        line += '\n'
        line += str(self.trans_prob)
        line += "\nemission_prob:\n"
        line += str(np.array(self.emission_prob).shape)
        line += '\n'
        line += str(self.emission_prob)
        line += "\n"
        return line

# degree of similarity(please check report if need)
def similarity(chord, obs):
    # print(chord, obs)
    sc = [5, 3, 2, 1]
    score = 0
    idx = [i for i, x in enumerate(chord) if x == 1]
    for i in range(len(idx)):
        score += obs[idx[i]] * sc[i]
        """
        if obs[idx[i]] == 1:
            score += sc[i]        
        """

    return score


# parse string into vector
# s = [chord keys]
def parser(s):
    if (len(s) < 1):
        return []
    vec = [0] * dimension
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

# generate rules for parameters initialization
def general_rules():
    keys = [v for v in CHORD.keys() if v != 'Nah']
    keys.sort()
    rules = []
    for k in keys:
        lookupstr = "C " + str(k)
        rule = lookupA(lookupstr)
        rules.append(parser(rule))
        print(lookupstr, rule, parser(rule))
    return rules

# convert string to vector
def praservec(s):
    vec = [0] * dimension
    vec_list = s.split(',')
    for i in range(len(vec_list)):
        t = str(vec_list[i])
        t = t.replace("[", "")
        t = t.replace("]", "")
        t = t.replace(" ", "")
        vec[i] = int(t)
        """
        if '1' in vec_list[i]:
           vec[i] = 1       
        """

    return vec

# encode data to fit MultinomialHMM
def encode_data(train_data):
    data = []
    for dt in train_data:
        for d in dt:
            print(d)
            if (len(d) >= 5):
                vec = praservec(d)
                if not (vec in data):
                    data.append(vec)
    return data

def code(data, table):
    return table.index(data)

def decode(data, table):
    return table[data]

# calculate accuracy
def accuracy(model, data, label):
    log = []
    a = []
    sa = []
    count = 0
    keys = model.states

    for idx, d in enumerate(data):
        print(idx)
        res = model.predict(d)
        corr = 0
        scorr = 0
        for id, i in enumerate(res[1]):
            l = ""
            l += d[id]
            l += "   "
            l += str(label[idx][id])
            l += "   "
            l += keys[i]
            log.append(l)

            print(keys[i], label[idx][id])
            if keys[i] == label[idx][id]:
                corr += 1
                scorr += 1
            elif keys[i] + '+' == label[idx][id]:
                scorr += 1
            elif keys[i] == label[idx][id] + '+':
                scorr += 1
        a.append(corr)
        sa.append(scorr)
        count += len(label[idx])

    return (np.sum(a) / count, np.sum(sa)/count), log

def chordIdentification(filepath):

    pos, data, label = utils.load_data(filepath)

    table = encode_data(data)
    # train model
    train_data = data[:-10]
    train_label = label[:-10]

    model = hmm(len(table), table)
    rules = general_rules()

    print('rules')
    print(rules)
    model.initialize_prob(rules)
    # data = load_train_files()
    model.update_prob(train_label)

    trans_p = utils.read_trans_prob("TRAN_PROB.csv")
    model.e_trans_prob(trans_p)

    # tr_data, tr_label = utils.load_data('test_data.csv')
    te_data = []
    te_label = []
    for i in range(len(data)):
        te_data.append(data[i])
        te_label.append(label[i])

    print("te_data:", te_data)
    model.fit(train_data)

    print(te_label)

    # test last 10 chords
    te = [x for x in range(len(te_data)-10, len(te_data))]
    t_data = [te_data[v] for v in te]
    t_label = [te_label[v] for v in te]
    (acc, sacc), log = accuracy(model, t_data, t_label)
    print(acc)

    accstr = "{:.2f}".format(acc)
    saccstr = "{:.2f}".format(sacc)

    sres = "Hard: "
    sres += accstr
    sres += " Soft: "
    sres += saccstr

    pos_t = [pos[t] for t in te]
    pos_x = []
    for p in pos_t:
        for x in p:
            pos_x.append(x)
    full_log = []
    for t, l in enumerate(log):
        # print(l)
        # print(pos_x[t])
        s = pos_x[t] + "  " + l
        full_log.append(s)

    return sres, full_log

if __name__ == '__main__':

    chordIdentification(sys.argv[1])