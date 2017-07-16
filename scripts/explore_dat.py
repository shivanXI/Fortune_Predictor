from collections import Counter
from matplotlib import pyplot as plt
import csv

DICTIONARY_FILENAME = 'data/CollegeScorecardDataDictionary-09-12-2015.csv'
DATA_FILENAME = 'data/MERGED2011_PP.csv'
NAME_KEY_INDEX = 3

def is_null(row, key, count_private_as_null = True):
	return row[key] == 'NULL' or (count_private_as_null and row[key] == 'PrivacySuppressed')
