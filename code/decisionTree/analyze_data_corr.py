import sys
import numpy as np
import random
import re
from scipy.stats import pearsonr
from sklearn.preprocessing import Imputer

def data_correlation():
	print "Using diabetes dataset"
	datafile = open("../../data/dataset_diabetes/original_data.csv")
	datalines = datafile.readlines()
	datafile.close()
	headers = datalines[0].strip().split(",")
	datalines = datalines[1:] # remove the headers
	readmissions = []
	no_readmissions = []
	for row in datalines:
		row = row.strip().split(",")
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
		if(index not in [18,19,20]): #remove diag columns bc their values are a mixed of strings and numbers
			if(not re.match("^\d+",col[0])):
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
	print data_by_col[-1][0:100]
	for i in range(len(data_by_col)-1):
		print headers[i], pearsonr(data_by_col[i], data_by_col[-1])[0]

data_correlation()