import sys
import numpy as np
import random
import csv
from scipy.stats import pearsonr
from sklearn.preprocessing import Imputer
import collections

sys.path.append('../data/dataset_diabetes')
import DatabaseManager

def data_correlation():
	print "Using diabetes dataset"
	#remove 'encounter_id', 'patient_nbr', diag_1', 'diag_2' and 'diag_3'
	#the last 3 are removed because they are a mix of numbers and strings
	left_out_features = ['encounter_id', 'patient_nbr', 'diag_1', 'diag_2', 'diag_3', 'examide', 'citoglipton']

	features_to_encode = ['race', 'gender', 'age', 'weight', 'payer_code', 'medical_specialty', 'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide', 'insulin', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone', 'change', 'diabetesMed']
	
	data_reader = csv.reader(open("../data/dataset_diabetes/original_data.csv", "rb"))
	features = data_reader.next()

	indexes_to_correlate = [index for (index, f) in enumerate(features) if f not in left_out_features]
	headers = [features[j] for j in indexes_to_correlate]

	indexes_to_encode = [index for (index, f) in enumerate(headers) if f in features_to_encode]

	readmissions = []
	no_readmissions = []
	for row in data_reader:
		row = [row[j] for j in indexes_to_correlate]
		if(row[-1]=='Yes'):
			row[-1] = 1
			readmissions.append(row)
		else:
			row[-1] = 0
			no_readmissions.append(row)

	print 'number of readmissions:', len(readmissions)
	sub_set = random.sample(no_readmissions, len(readmissions)) + readmissions   
	
	temp_data_mat = np.array(sub_set)

	# We need to convert categorical data to ints/floats so we can use one hot encoding
	data_mat = []
	for (index, col) in enumerate(temp_data_mat.T):
		if(index in indexes_to_encode):
			unique_vals = []
			for (ii, item) in enumerate(col):
				if item not in unique_vals:
					unique_vals.append(item)
				
				if item == "?":
					col[ii] = "NaN"
				else:
					col[ii] = unique_vals.index(item)  
		data_mat.append(col)

	# # convert out of the column format
	data_mat = np.array(data_mat).T


	# Imputer converts missing values (?'s) to the mean of the column
	#   mean, median, and mode are available options for strategy
	imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
	data_mat = imp.fit_transform(data_mat)

	np.random.shuffle(data_mat)
	data_by_col = data_mat.T


	d = {}
	for i in range(len(data_by_col)-1):
		corre = pearsonr(data_by_col[i], data_by_col[-1])[0]
		d[abs(corre)] = [corre, headers[i]]

	od = collections.OrderedDict(reversed(sorted(d.items())))
	for v in od.values():
		print v

data_correlation()