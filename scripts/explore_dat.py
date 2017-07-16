from collections import Counter
from matplotlib import pyplot as plt
import csv

DICTIONARY_FILENAME = 'data/CollegeScorecardDataDictionary-09-12-2015.csv'
DATA_FILENAME = 'data/MERGED2011_PP.csv'
NAME_KEY_INDEX = 3

def is_null(row, key, count_private_as_null = True):
	return row[key] == 'NULL' or (count_private_as_null and row[key] == 'PrivacySuppressed')


def explore_nulls(keys, rows):
	debt_key = keys.index('GRAD_DEBT_MDN')
	earnings_key = keys.index('MD_EARN_WNE_P6')
	degrees_key = keys.index('CIP01ASSOC')
	pcip_key = keys.index('PCIP01')

	'''
	Below is nested single line for loop.
	return: rows which have non-NULL values in all specified columns
	'''
	rows = [row for row in rows if(
				not is_null(row, debt_key)
				and not is_null(row, earnings_key)
				and not is_null(row, degrees_key)
				and not is_null(row, pcip_key)
			)]

	#
