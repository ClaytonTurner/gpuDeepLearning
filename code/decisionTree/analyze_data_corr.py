import sys
import numpy as np
import random
import re
from scipy.stats import pearsonr
from sklearn.preprocessing import Imputer

def data_correlation():
    print "Using diabetes dataset"
    datafile = open("../../data/dataset_diabetes/subset_features_data.csv")
    datalines = datafile.readlines()
    datafile.close()
    headers = datalines[0].strip().split(",")
    datalines = datalines[1:] # remove the headers
    for (i, row) in enumerate(datalines):
        datalines[i] = row.strip().split(",")
        
    temp_data_mat = np.array(datalines)

    # We need to convert categorical data to ints/floats so we can use one hot encoding
    data_mat = []
    for col in temp_data_mat.T:
        unique_vals = []
        for (ii, item) in enumerate(col):
            if item not in unique_vals:
                unique_vals.append(item)
            
            if item == "?":
                col[ii] = "NaN"
            elif not re.match("^\d+",item):
                col[ii] = unique_vals.index(item)  
        data_mat.append(col)

    # # convert out of the column format
    data_mat = np.array(data_mat).T


    # Imputer converts missing values (?'s) to the mean of the column
    #   mean, median, and mode are available options for strategy
    imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
    data_mat = imp.fit_transform(data_mat)

    data_by_col = data_mat.T
    for i in range(len(data_by_col)-1):
        print i
        print headers[i], pearsonr(data_by_col[i], data_by_col[-1])[0]

data_correlation()