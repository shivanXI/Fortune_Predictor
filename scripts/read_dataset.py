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


def get_all_rows(data_file_name=DEFAULT_DATASET_NAME):
    with open(data_file_name, 'r') as data_file:
        # reader = csv.reader(data_file)
        # rows = [row for row in csv.reader(data_file)]
        rows = data_file.readlines()
        for i in xrange(len(rows)):
            if rows[i].startswith(codecs.BOM_UTF8):
                rows[i] = rows[i][len(codecs.BOM_UTF8):]
            rows[i] = rows[i].strip().split(',')
        return rows[1:], rows[0]
