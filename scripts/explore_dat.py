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

	#counts number of null using inline for loop
	num_null = {key:0 for key in keys}

	both_debt_and_earnings_count= 0
	max_key_index = keys.index('RPY_1YR_RT')

	for rows in rows:
		'''
		Count the number of non-NULL debt_key and earnings_key rows
		'''
		if not (row[debt_key] == 'NULL' or row[debt_key] == 'PrivacySuppressed') and not (
		row[earnings_key] == 'NULL' or row[earnings_key] == 'PrivacySuppressed'):
			both_debt_and_earnings_count += 1
		'''
		xrange() generate xrange object list - which is non-static
		instead of range() which generate static list object -resulting in
		memory overflow.

		xrange(start, stop, step)
		'''

		for i in xrange(max_key_index):
			if is_null(row, i):
				num_null[keys[i]] += 1
