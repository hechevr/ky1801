from sklearn import tree
import utils

def praservec(s):
    vec = [0] * 7
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

# load data
pos, data, label = utils.load_data("Mozart1_standard_L.csv")


keys = [v for v in utils.CHORD.keys()]
keys.sort()

print(keys)

train_data = []
train_label = []
train_label_idx = []
for i in range(len(data)):
    for j in range(len(data[i])):
        train_data.append(praservec(data[i][j]))
        train_label.append(label[i][j])
        train_label_idx.append(keys.index(label[i][j].replace(" ", "")))

for i in range(len(train_data)):
    print(train_data[i], train_label[i], train_label_idx[i])




test_data = train_data[:10]
test_label = train_label_idx[:10]
train_data = train_data[10:]
train_label = train_label_idx[10:]
model = tree.DecisionTreeClassifier()
model.fit(train_data, train_label)

res = model.predict_proba(test_data)

print(res)
print(test_label)
