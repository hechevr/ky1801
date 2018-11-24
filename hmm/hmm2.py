import numpy as np
from utils import CHORD, load_train_files
import hmmlearn.hmm as hmm_model
from lookup import lookupA
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

class hmm(object):
    def __init__(self, n_obs=2**7):
        # states = [chord + 'Nah'] = [22]
        self.states = [v for v in CHORD.keys()]
        self.states.sort()
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

    def fit(self, data):
        self.update_start_prob(data)
        self.update_trans_prob(data)
        self.update_emission_prob(data)

        self.hmm = hmm_model.MultinomialHMM(n_components=self.n_states)
        self.hmm.startprob_ = self.start_prob
        self.hmm.transmat_ = self.trans_prob
        self.hmm.emissionprob_ = self.emission_prob

    def predict(self, observations, option='vertibi'):

        return self.hmm.decode(observations, algorithm=option)


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
        self.trans_prob += 1.0 / (self.n_states * self.n_states)

    def initialize_emission_prob(self, data):
        # emission_prob = emission probability
        self.emission_prob = np.zeros((self.n_states, self.n_obs), dtype=np.float32)
        self.emission_prob += 1.0 / self.n_obs

        for i in range(len(data)):
            if (len(data[i]) > 0):
                self.emission_prob[i][self.vec2obs(data[i])] += 1
        self.emission_prob /= np.sum(self.emission_prob, axis=0)

    # initialize start_prob
    def update_start_prob(self, data):

        chord_list = data[:, 1]
        for chord in chord_list:
            if (chord in CHORD.keys()):
                self.start_prob[CHORD[chord]] += 1

        # normalize
        self.start_prob = self.start_prob / self.start_prob.sum()
        return self.start_prob

    # initialize transition prob
    def update_trans_prob(self, data):
        return self.trans_prob

    # initialize emission prob
    def update_emission_prob(self, data):

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

        return self.emission_prob

    def __str__(self):
        line = "hmm model for chord identification"
        line += "\nstates:\n"
        line += str(self.states)
        line += "\nobservations:\n"
        line += str(self.observations)
        line += "\nstart_prob:\n"
        line += str(self.start_prob)
        line += "\ntrans_prob:\n"
        line += str(self.trans_prob)
        line += "\nemission_prob:\n"
        line += str(self.emission_prob)
        line += "\n"
        return line

# parse string into vector
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

def general_rules():
    keys = [v for v in CHORD.keys() if v != 'Nah']
    keys.sort()
    rules = [[]]
    for k in keys:
        lookupstr = "C " + str(k)
        rule = lookupA(lookupstr)
        rules.append(parser(rule))
    return rules

if __name__ == '__main__':
    model = hmm()
    rules = general_rules()

    print(rules)

    model.initialize_prob(rules)
    data = load_train_files()
    model.fit(data)

    print(model)


