import sys
import cPickle as pickle
import gzip
import numpy as np
from sklearn.preprocessing import Imputer, OneHotEncoder
import re
import random

def pickle_data():
    """
    This single-function file is for pickling datasets to be sent to each algorithm
    """

    # The goal is to predict readmission
    print "Using diabetes dataset"
    datafile = open("../../data/dataset_diabetes/formatted_diabetic_data.csv")
    datalines = datafile.readlines()
    datafile.close()
    datalines = datalines[1:] # remove the headers
    readmissions = []
    no_readmissions = []
    for row in datalines:
        row = row.strip().split(",")
        #row = [row[j] for j in [0,2,3,4,8,9,10,15]] #decision tree

        if(row[-1] == 'Yes'):
            readmissions.append(row)
        else:
            no_readmissions.append(row)

    sub_set = random.sample(readmissions, 10000) + random.sample(no_readmissions, 10000)       
    temp_data_mat = np.matrix(sub_set)
    # We need to convert categorical data to ints/floats so we can use one hot encoding
    data_mat = []
    for col in temp_data_mat.T:
        unique_vals = []
        col_list = col.tolist()
        for ii in range(len(col_list)):
            for i in range(len(col_list[ii])):
                item = col_list[ii][i]
                if item not in unique_vals:
                    unique_vals.append(item)
                
                if item == "?":
                    col_list[ii][i] = "NaN"
                elif not re.match("^\d+",item):
                    col_list[ii][i] = unique_vals.index(item)   
        data_mat.append(col_list[0])

    # # convert out of the column format
    data_mat = np.array(data_mat).T
    
    # Imputer converts missing values (?'s) to the mean of the column
    #   mean, median, and mode are available options for strategy
    imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
    data_mat = imp.fit_transform(data_mat)

    # OneHotEncode categorical features so we can use them in NNs
    # categorical_feats = [0,1,2,11,12,13,14]
    # encoder = OneHotEncoder(categorical_features=categorical_feats, sparse=False)
    # data_mat = encoder.fit_transform(data_mat)


    np.random.shuffle(data_mat)

    y = data_mat[:,-1]
    x = data_mat[:,:-1]
    print "y:", y
    print "x:", x
    print "Feature count after encoding:",len(x[0])

    # Let's split the data into training, validation, and testing
    test_start = 0
    test_end = int(len(x)*0.3)
    test_matrix = x[test_start:test_end]
    test_labels = y[test_start:test_end]
    training_matrix = np.delete(x, [i for i in range(test_start, test_end)], 0)
    training_labels = np.delete(y, [i for i in range(test_start, test_end)], 0)

    # Now let's compress the data to a .pkl.gz for logistic_sgd's load_data()
    pickle_array = [[training_matrix, training_labels],
                    [test_matrix, test_labels]]
    fname = "diabetes.pkl.gz"
    f = gzip.open(fname, "wb")
    pickle.dump(pickle_array, f)
    f.close()


pickle_data()