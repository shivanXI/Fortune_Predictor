from sklearn.ensemble import RandomForestClassifier
import pandas as pd

train = pd.read_csv("train_feature_data.csv")
test = pd.read_csv("train_feature_data.csv")
default = pd.read_csv("default_outcome_data.csv")
cols = [0, 1, 2, 3]
colres = [0]
