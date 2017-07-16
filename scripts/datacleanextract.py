import csv
import math
import codecs
import read_dataset

DEFAULT_DATASET_NAME = 'MERGED2011_12_PP.csv'

REQUIRED_LABEL_KEYS = [
    'GRAD_DEBT_MDN',
    'MD_EARN_WNE_P6',
    'CIP01ASSOC',
    'PCIP01',
    'MN_EARN_WNE_INC1_P10',
]

def is_null(row, key_index, count_private_as_null=False):
    return row[key_index] == 'NULL' or (count_private_as_null and row[key_index] == 'PrivacySuppressed')

def get_required_features(label_keys = REQUIRED_LABEL_KEYS):
    
    features = list()
    features_data = list()
    default_outcome_data = list()
    default_outcome_dataset = list()
    train_features = list()
    train_features_data = list()
    
    rows, keys = read_dataset.get_filtered_rows()

    with open(DEFAULT_DATASET_NAME, 'r') as data_file:
        all_keys = [row for row in csv.reader(data_file)]

    label_indices = [keys.index(label_key) for label_key in label_keys]

    for row in rows:
        for i in xrange(len(label_indices)):
            features.append(row[label_indices[i]])

    for j in xrange(len(features)):
        if features[j] == 'PrivacySuppressed':
            features[j] = -1.0
        if is_null(features, j):
            features[j] = 0.0

    it = iter(features)
    features_data = zip(it,it,it,it,it)

    #print len(features_data)

    for k in xrange(len(features_data)):
            data = features_data[k]
            default_outcome_dataset.append(data[len(data)-1])

    #print default_outcome_dataset
    it2 = iter(default_outcome_dataset)
    default_outcome_data = zip(it2)

    print len(default_outcome_data)

    for u in xrange(len(features_data)):
        data = features_data[u]
        for h in xrange(len(data)):
            if(h != len(data)):
                train_features.append(data[h])

    it1 = iter(train_features)
    train_features_data = zip(it1, it1, it1, it1)

    #print train_features_data


    with open('train_feature_data.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(train_features_data)

    with open('default_outcome_data.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(default_outcome_data)

    with open('all_feature_data.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(features_data)
    
                
