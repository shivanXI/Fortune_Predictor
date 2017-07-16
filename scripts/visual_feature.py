import csv
import math
import codecs
import read_dataset
import numpy 

DEFAULT_DATASET_NAME = 'MERGED2011_12_PP.csv'

UNIVERSITY_NAME_KEY = [
    'INSTNM',
    'CITY'
]

REQUIRED_INCOME_KEYS = [
    'MN_EARN_WNE_INC1_P10',
    'MN_EARN_WNE_INC2_P10',
    'MN_EARN_WNE_INC3_P10',
    'MN_EARN_WNE_INDEP1_P10',
    'MN_EARN_WNE_MALE0_P10',
    'MN_EARN_WNE_MALE1_P10'
]

def is_null(row, key_index, count_private_as_null=False):
    return row[key_index] == 'NULL' or (count_private_as_null and row[key_index] == 'PrivacySuppressed')


def get_required_features(label_keys = REQUIRED_INCOME_KEYS, univ_keys = UNIVERSITY_NAME_KEY):

    avg = list()
    features = list()
    features_data = list()
    univ_data = list()
    default_outcome_data = list()
    average_income_dataset = list()
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
    features_data = zip(it,it,it,it)

    #print features_data

    for k in xrange(len(features_data)):
            data = features_data[k]
            #for j in xrange(len(data)):
            print numpy.array(data)
            #average_income_dataset.append(numpy.mean(numpy.array(data)))

    univ_indices = [keys.index(univ_key) for univ_key in univ_keys]

    for row in rows:
        for p in xrange(len(univ_indices)):
            univ_data.append(row[univ_indices[p]])

     

    it3 = iter(univ_data)
    #it2 = iter(average_income_dataset)

    average_income_data = zip(it3,it3)
    print average_income_data
    #print univ_data

    with open('university_data.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerows(univ_data)
