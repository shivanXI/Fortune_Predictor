import csv
import read_dataset


DICTIONARY_FILENAME = 'MERGED2011_12_PP.csv'

LABEL_KEYS = [
    'GRAD_DEBT_MDN',
    'MD_EARN_WNE_P6',
]

REQUIRED_LABEL_KEY = [
    'MN_EARN_WNE_INC1_P10',
]

def is_null(row, key_index, count_private_as_null=False):
    return row[key_index] == 'NULL' or (count_private_as_null and row[key_index] == 'PrivacySuppressed')


def is_prediction_key(key_row):
    # 'aid' fields that are not prediction keys
    if key_row[0] in ['pell_grant_rate', 'PCTFLOAN', 'loan_ever']:
        return True
    return key_row[2] in ['repayment', 'earnings', 'aid']

def is_category(key_row):
    return not key_row[0] and not key_row[1]


def get_categorical_keys(key_rows):
    categorical_keys = {}
    current_category_key = None
    current_categories = []
    for row in key_rows:
        if current_category_key:
            if is_category(row):
                current_categories.append((row[7], row[8]))
            else:
                if len(current_categories) > 0:
                    categorical_keys[current_category_key] = current_categories
                current_category_key = row[4]
                current_categories = []
        elif not is_category(row):
            current_category_key = row[4]
            current_categories = []
        else:
            print 'ERROR: saw category before key'
    return categorical_keys
