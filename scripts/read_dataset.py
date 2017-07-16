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

def get_filtered_rows(data_file_name=DEFAULT_DATASET_NAME, required_keys=DEFAULT_REQUIRED_KEYS, get_unlabeled=True):
    '''Return all rows that have non-NULL/PrivacySuppressed entries for all required keys.'''
    all_rows, keys = get_all_rows(data_file_name=data_file_name)
    required_indices = [keys.index(key) for key in required_keys]
    filtered_rows = []
    for row in all_rows:
        has_null_required = any([is_null(row, i) for i in required_indices])
        if (get_unlabeled and has_null_required) or ((not get_unlabeled) and (not has_null_required)):
            filtered_rows.append(row)

    with open('all_labels.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerows(keys)
            
    return filtered_rows, keys

if __name__=='__main__':
    all_rows, keys = get_all_rows()
    filtered_rows, keys2 = get_filtered_rows()
    assert keys == keys2

    with open('all_labels.csv', 'w') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerows(keys)

    print 'Filter step selected %s of %s rows' % (len(filtered_rows), len(all_rows))


