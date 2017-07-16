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
