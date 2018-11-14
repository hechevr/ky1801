import numpy as np
import os
import sys

from hmmlearn import hmm

from hmm import CHORD_IN_VEC
from hmm import CHORD_LIST

from hmm import load_train_files
from hmm import vec2dec
from hmm import dec2vec
from hmm import hmm_shit

from sklearn.preprocessing import LabelEncoder


states = ['I', 'I+', 'IIb', 'II', 'II7', 'III', 'IV', 'V', 'V7', 'V+', 'V+7', 'VIb', 'VI', 'VI7', 'VIGer', 'VII', 'VII7', 'VIIGer', 'VIIIta', 'VIIdim', 'VIIdim7']
n_states = len(states)

observations = [o for o in range(4096)]
n_observations = len(observations)

data = load_train_files()



X = []
labels = []
for f in data:
    for v in f:
        print(v)
        # print(v)
        # print(vec2dec(v[0]))
        # X.append(vec2dec(v[0]))
        X.append(v[0])
        labels.append(v[1])
        
X = np.array(X)

model = hmm.MultinomialHMM(n_components=n_states, n_iter=20, tol=0.01)
# model = hmm.GMMHMM(n_components=n_states, n_iter=100)
# model.n_features = n_observations
# model.n_symbols = n_observations


obs = []
for x in X:
    obs.append(vec2dec(x))


start_prob, trans_prob, emission_prob = hmm_shit()

start_prob = np.array(start_prob)
start_prob = np.reshape(start_prob, (len(start_prob[0])))
print(np.array(start_prob).sum())
model.startprob_ = start_prob[0]
model.transmat_ = trans_prob
model.emissionprob = emission_prob


le = LabelEncoder()
le.fit(obs)

train_obs = le.transform(obs)
print(train_obs)

train_obs = np.reshape(train_obs, (1, -1))

for i in range(100):
    model.fit(train_obs)
    
train_obs = np.reshape(train_obs, (-1, 1))
prob, box = model.decode(train_obs, algorithm='viterbi')

print(box)
print([states[b] for b in box])
print(prob)

"""
correct = 0
for i in range(len(labels)):
    correct += (states[box[i]] == labels[i])
    # print(states[box[i]])
    # print(dec2vec(int(obs[i])))
    # print(X[i])
    # print(states[box[i]], labels[i])
print(correct * 1.0 / len(labels))
"""
