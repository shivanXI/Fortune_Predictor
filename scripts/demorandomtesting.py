from sklearn.ensemble import RandomForestClassifier
import pandas as pd

train = pd.read_csv("train_feature_data.csv")
test = pd.read_csv("train_feature_data.csv")
default = pd.read_csv("default_outcome_data.csv")
cols = [0, 1, 2, 3]
colres = [0]


#label_indices = [keys.index(label_key) for label_key in label_keys]

trainArr = train.as_matrix(cols)
trainRes = train.as_matrix(colres)


rf = RandomForestClassifier(n_estimators=100)
rf.fit(trainArr, trainRes)
