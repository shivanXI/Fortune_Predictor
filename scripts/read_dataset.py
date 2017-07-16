'''
Data Reading Module
This module is responsible for reading educational data for a certain year and optionally filtering out all schools which do not have data present in a given set of feilds.
'''

import codecs
import csv

DEFAULT_DATASET_NAME = 'MERGED2011_12_PP.csv'

DEFAULT_REQUIRED_KEYS = [
	'GRAD_DEBT_MDN',
	'MD_EARN_WNE_P6',
        'MN_EARN_WNE_INC1_P10',
]

def is_null(row, key_index, count_private_as_null = True):
	return row[key_index] == 'NULL' or (count_private_as_null and row[key_index] == 'PrivacySuppressed')
