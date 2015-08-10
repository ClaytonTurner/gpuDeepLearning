__author__ = 'caturner3'

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
    if(len(sys.argv) <= 2):
        print >> sys.stderr, "Proper usage of subSet_pickle_data.py: subSet_pickle_data.py <dataset> <tenth of dataset for testing>"
        sys.exit(1)
    dataset = sys.argv[1]
    tenth = float(sys.argv[2])
    td_amt = .80 # training data amount - inverse is validation amount
    if dataset == "diabetes":
        # The goal is to predict readmission
        print "Using "+dataset+" dataset"
        datafile = open("../data/dataset_diabetes/diabetic_data_2outs.csv")
        datalines = datafile.readlines()
        datafile.close()
        datalines = datalines[1:] # remove the headers
        readmitted_list = []
        no_readmitted_list = []
        for row in datalines:
            # select a sub set o features
            row = row.strip().split(",")
            row = [row[j] for j in [6,7,8,12,16,17,21,49]]

            if(row[-1] == '<30'):
                readmitted_list.append(row)
            else:
                no_readmitted_list.append(row)

        sub_set = random.sample(readmitted_list, 1000) + random.sample(no_readmitted_list, 1000)       
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
                    if item != "?" and not re.match("^\d+",item):
                        col_list[ii][i] = unique_vals.index(item)
                    elif item == "?":
                        col_list[ii][i] = "NaN"
            data_mat.append(col_list[0])

        # convert out of the column format
        data_mat = np.array(data_mat).T
        np.random.shuffle(data_mat)
        # Imputer converts missing values (?'s) to the mean of the column
        #   mean, median, and mode are available options for strategy
        imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
        data_mat = imp.fit_transform(data_mat)
        # OneHotEncode categorical features so we can use them in NNs
        categorical_feats = [0, 1, 2]
        encoder = OneHotEncoder(categorical_features=categorical_feats, sparse=False)
        data_mat = encoder.fit_transform(data_mat)
        y = data_mat[:,-1]
        x = data_mat[:,:-1]
        print "y:", y
        print "x:", x
        print "Feature count after encoding:",len(x[0])

    elif dataset == "heritage":
        print "Using "+dataset+" dataset"
    elif dataset == "pubmed":
        print "Using "+dataset+" dataset"
    else:
        print "Improper dataset specified"
        sys.exit(1)

    # Let's split the data into training, validation, and testing
    rows = len(x)
    kfold = 10 # Assuming 10-fold cross validation for everything
    test_start = int((tenth-1)*rows/kfold)
    test_end = int((tenth)*rows/kfold)
    test_matrix = x[test_start:test_end]
    test_labels = y[test_start:test_end]
    training_matrix = np.delete(x, [i for i in range(test_start, test_end)], 0)
    training_labels = np.delete(y, [i for i in range(test_start, test_end)], 0)
    # Validation after testing so we don't have to worry about the meshing
    #   of validation and testing data
    valid_matrix = x[(td_amt*rows):]
    valid_labels = y[(td_amt*rows):]

    # Now let's compress the data to a .pkl.gz for logistic_sgd's load_data()
    pickle_array = [[training_matrix, training_labels],
                    [valid_matrix, valid_labels],
                    [test_matrix, test_labels]]
    fname = "../data/diabetes.pkl.gz"
    f = gzip.open(fname, "wb")
    pickle.dump(pickle_array, f)
    f.close()


pickle_data()