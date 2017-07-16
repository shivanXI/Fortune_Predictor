import csv
import numpy as np
import random
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

FEATURES_FILENAME = 'all_features.csv'
LABELS_FILENAME = 'all_labels.csv'
DATA_SPLIT_FILENAME = ''
DEFAULT_OUTCOME_FILENAME = 'default_outcome_label.csv'

def read_features_and_labels(features_filename=FEATURES_FILENAME, labels_filename=LABELS_FILENAME, feature_selection=None, use_privacy_suppressed=False):
    if use_privacy_suppressed:
        feature_names = None
        with open(features_filename, 'r') as features_file:
            raw_rows = [row for row in csv.reader(features_file)]
            feature_rows = [[float(val) for val in row] for row in raw_rows]
    else:
        with open(features_filename, 'r') as features_file:
            raw_rows = [row for row in csv.reader(features_file)]
            feature_names = raw_rows[0]
            feature_rows = [[float(val) for val in row] for row in raw_rows[1:]]
            if feature_selection:
                with open(feature_selection, 'r') as f:
                    indices = [int(s.strip()) for s in f.read().strip().split(',')]
                feature_rows = [[v for i, v in enumerate(row) if indices[i]] for row in feature_rows]
    with open(labels_filename, 'r') as labels_file:
        raw_rows = [row for row in csv.reader(labels_file)]
        label_names = raw_rows[0]
        label_rows = [[float(val) for val in row] for row in raw_rows[1:]]
    return feature_names, feature_rows, label_names, label_rows
