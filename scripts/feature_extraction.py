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

def get_non_feature_keys(rows, keys, key_row_lookup):
    prediction_keys = set([
        key for key in keys
        if key in key_row_lookup and is_prediction_key(key_row_lookup[key])
    ])
    cohort_size_keys = set([
        key for key in keys
        if key.endswith('_N')
    ])
    all_null_keys = set([
        keys[i] for i in xrange(len(keys))
        if all([is_null(row, i) for row in rows])
    ])
    non_numerical_keys = set(['INSTNM', 'STABBR', 'ZIP', 'CITY'])

    non_feature_keys = prediction_keys.union(
        cohort_size_keys).union(
        all_null_keys).union(
        non_numerical_keys)
    return non_feature_keys

def get_examples(label_keys=LABEL_KEYS):
    rows, keys = read_dataset.get_filtered_rows()

    with open(DICTIONARY_FILENAME, 'r') as dict_file:
        key_rows = [row for row in csv.reader(dict_file)][1:]
    key_row_lookup = {key_row[4]: key_row for key_row in key_rows if key_row[4]}

    non_feature_keys = get_non_feature_keys(rows, keys, key_row_lookup)
    privacy_suppressed_keys = set([
        keys[i] for i in xrange(len(keys))
        if any([row[i] == 'PrivacySuppressed' for row in rows])
    ])
    categorical_keys = get_categorical_keys(key_rows)

    label_indices = [keys.index(label_key) for label_key in label_keys]

    examples = []
    privacy_suppressed_values = []

    for row in rows:
        features = {}
        privacy_suppressed_features = {}
        for i in xrange(len(keys)):
            if keys[i] not in non_feature_keys:
                if keys[i] in privacy_suppressed_keys:
                    if is_null(row, i):
                        value = 0.0
                    elif row[i] == 'PrivacySuppressed':
                        value = -1.0
                    else:
                        value = row[i]
                    privacy_suppressed_features[keys[i]] = value
                else:
                    is_null_key = '%s_is_NULL' % (keys[i])

                    if keys[i] in categorical_keys:
                        category_value_is_null = is_null(row, i)
                        features[is_null_key] = 1.0 if category_value_is_null else 0.0
                        for category_value, category_label in categorical_keys[keys[i]]:
                            category_key = '%s = %s' % (keys[i], category_label)
                            features[category_key] = (
                                1.0 if not category_value_is_null and row[i] == category_value
                                else 0.0
                            )

                    else: # Non-categorical keys
                        # TODO: alternative ways of dealing with PrivacySuppressed?
                        if is_null(row, i):
                            features[keys[i]] = 0.0
                            features[is_null_key] = 1.0
                        else:
                            features[keys[i]] = row[i]
                            features[is_null_key] = 0.0

        # Arrange features alphabetically for more consistent ordering
        # between runs and easier exploration of the fitted model
        feature_values = [features[key] for key in sorted(features)]
        try:
            labels = [float(row[label_index]) for label_index in label_indices]
        except ValueError:
            labels = [row[label_index].strip() for label_index in label_indices]
        examples.append((feature_values, labels))
        privacy_suppressed_values.append([privacy_suppressed_features[key] for key in sorted(privacy_suppressed_features)])

    return examples, sorted(features), label_keys, privacy_suppressed_values, sorted(privacy_suppressed_features)


def get_required_label(label_keys=REQUIRED_LABEL_KEY):
    
    rows, keys = read_dataset.get_filtered_rows()

    with open(DICTIONARY_FILENAME, 'r') as dict_file:
        key_rows = [row for row in csv.reader(dict_file)][1:]
    key_row_lookup = {key_row[4]: key_row for key_row in key_rows if key_row[4]}

    non_feature_keys = get_non_feature_keys(rows, keys, key_row_lookup)
    privacy_suppressed_keys = set([
        keys[i] for i in xrange(len(keys))
        if any([row[i] == 'PrivacySuppressed' for row in rows])
    ])
    #categorical_keys = get_categorical_keys(key_rows)

    label_indices = [keys.index(label_key) for label_key in label_keys]

    #examples = []
    #privacy_suppressed_values = []

    for row in rows:
        features = {}
        #privacy_suppressed_features = {}
        for i in xrange(len(keys)):
            if keys[i] not in non_feature_keys:
                if keys[i] in privacy_suppressed_keys:
                    if is_null(row, i):
                        value = 0.0
                    elif row[i] == 'PrivacySuppressed':
                        value = -1.0
                    else:
                        value = row[i]
                    #privacy_suppressed_features[keys[i]] = value
                else:
                    is_null_key = '%s_is_NULL' % (keys[i])

                    #if keys[i] in categorical_keys:
                        #category_value_is_null = is_null(row, i)
                        #features[is_null_key] = 1.0 if category_value_is_null else 0.0
                        #for category_value, category_label in categorical_keys[keys[i]]:
                            #category_key = '%s = %s' % (keys[i], category_label)
                            #features[category_key] = (
                                #1.0 if not category_value_is_null and row[i] == category_value
                                #else 0.0
                            #)

                    #else: # Non-categorical keys
                        # TODO: alternative ways of dealing with PrivacySuppressed?
                    if is_null(row, i):
                        features[keys[i]] = 0.0
                        features[is_null_key] = 1.0
                    else:
                        features[keys[i]] = row[i]
                        features[is_null_key] = 0.0

        # Arrange features alphabetically for more consistent ordering
        # between runs and easier exploration of the fitted model
        feature_values = [features[key] for key in sorted(features)]
        try:
            labels = [float(row[label_index]) for label_index in label_indices]
        except ValueError:
            labels = [row[label_index].strip() for label_index in label_indices]
        #examples.append((feature_values, labels))
        #privacy_suppressed_values.append([privacy_suppressed_features[key] for key in sorted(privacy_suppressed_features)])

    return feature_values

#print get_required_label()
all_feature = []
default_outcome_label = []
all_example = list()
feature = list()
labels = []

#privacy_suppressed_values = list()
#privacy_suppressed_features = list()
#all_feature.append(get_examples())
#all_example, feature, labels, privacy_suppressed_values, privacy_suppressed_features = get_examples()
#labels2 = get_required_label()
#privacy_suppressed_values.append([privacy_suppressed_features[key] for key in sorted(privacy_suppressed_features)])

'''all_feature = privacy_suppressed_values
for i in xrange(len(privacy_suppressed_features)):
       if privacy_suppressed_features[i] == 'MN_EARN_WNE_INC1_P10':
           default_outcome_label.append(privacy_suppressed_values[privacy_suppressed_features[i]])'''

default_outcome_label.append(get_required_label())
#print all_labels[0][2]
print default_outcome_label


