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


def normalize_features(feature_rows):
    for i in xrange(len(feature_rows[0])):
        values = [row[i] for row in feature_rows]
        mean = np.mean(values)
        std = np.std(values)
        for j in xrange(len(feature_rows)):
            feature_rows[j][i] = (feature_rows[j][i] - mean) / std




def get_data_splits(feature_rows, label_rows):
    with open(DATA_SPLIT_FILENAME, 'r') as f:
        indices = [int(row.strip()) - 1 for row in f]
    train_indices = set(indices[:3500])
    dev_indices = set(indices[3500:4500])
    train, dev, test = [], [], []
    for i in xrange(len(feature_rows)):
        example = (feature_rows[i], label_rows[i])
        if i in train_indices:
            train.append(example)
        elif i in dev_indices:
            dev.append(example)
        else:
            test.append(example)
    return train, dev, test

def get_knn_predictions(train, dev, k=5, weighting='uniform'):
    predictions = []
    train_indices = [i for i in xrange(len(train))]
    iters = 0
    print 'Using k=%s and %s weighting' % (k, weighting)

    for features, labels in dev:
        iters += 1
        if iters == 1 or iters % 100 == 0 :
            print '\tIteration %s of %s' % (iters, len(dev))

        features = np.array(features)
        distances = {}
        for i in train_indices:
            other_features = np.array(train[i][0])
            distances[i] = np.linalg.norm(features - other_features)
        neighbors = sorted(train_indices, key=distances.get)[:k]

        weights = {i: 1.0 / k for i in neighbors}
        if weighting == 'inverse_distance':
            sum_inv_distances = sum([1.0 / distances[i] for i in neighbors])
            weights = {i: (1.0 / distances[i]) / sum_inv_distances for i in neighbors}
        elif weighting != 'uniform':
            print 'Unknown weighting scheme %s; defaulting to uniform weights' % (weighting)

        predicted_labels = np.zeros(len(labels))
        for i in neighbors:
            predicted_labels += weights[i] * np.array(train[i][1])
        predictions.append(predicted_labels)
        return predictions

def get_naive_bayes_predictions(train, default_outcome, test):
    train_features = [features for features, labels in train]
    
    train_values = np.array(train_features)
    
    values = [values for values in default_outcome]
    
    outcome_values = np.array(values)
    
    predictions = []
    classifier = GaussianNB()
    classifier.fit(train_values, outcome_values)
    test_indices = [i for i in xrange(len(test))]
    for i in test_indices:
        predictions.append(classifier.predict([test[i]]))
    return predictions



    
    
def get_random_forest_predictions(train, default_outcome, test):
     train_features = [features for features, labels in train]
     train_values = np.array(train_features)
     values = [values for values in default_outcome]
     outcome_values = np.array(values)
     predictions = []
     
     model = RandomForestClassifier(n_estimators = 14)
     model.fit(train_values, outcome_values)
     test_indices = [i for i in xrange(len(test))]
     for i in test_indices:
        predictions.append(model.predict([test[i]]))

     return predictions



def compute_percent_errors(all_labels, all_predictions, use_rmse=False):
    num_labels = len(all_labels[0])
    all_errors = [[] for _ in xrange(num_labels)]
    for labels, predictions in zip(all_labels, all_predictions):
        '''
        INCOMPLETE


        '''

# To WRITE MAIN FILE
if __name__=='__main__':
    naive_bayes = list()
    random_forest = list()
    
    #############################
    file=open("train_feature_data.csv","r")
    data=list()
    for line in file:
        data.append(line.split('\n'))
    file.close()
    random.shuffle(data)
    train_data = data[:int((len(data)+1)*.80)] #Remaining 80% to training set
    test_data = data[int(len(data)*.80+1):] #Splits 20% data to test set

     ################################

    '''file_outcome=open("default_outcome_label.csv","r")
    data_outcome=list()
    for line in file_outcome:
        data_outcome.append(line.split('\n'))
    file_outcome.close()
    random.shuffle(data_outcome)
    default_outcome_data = data_outcome[:int((len(data_outcome)+1)*.80)]''' #Remaining 80% to training set

    naive_bayes = get_naive_bayes_predictions(train_data, test_data)
    random_forest = get_random_forest_predictions(train_data, test_data)

    print("NAIVE BAYES")
    print naive_bayes

    print("RANDOM_FOREST")
    print random_forest

