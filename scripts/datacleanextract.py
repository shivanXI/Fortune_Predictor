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

