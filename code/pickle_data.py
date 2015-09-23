__author__ = 'caturner3'

import sys
import cPickle as pickle
import gzip
import numpy as np
import re
import random
from sklearn import preprocessing
import csv

def pickle_data():
    """
    This single-function file is for pickling datasets to be sent to each algorithm
    """
    if(len(sys.argv) <= 1):
        print >> sys.stderr, "Proper usage of pickle_data.py: pickle_data.py <tenth of dataset for testing>"
        sys.exit(1)
    tenth = float(sys.argv[1])
    # The goal is to predict readmission
    print "Using diabetes dataset"
    data_reader = csv.reader(open("../data/dataset_diabetes/subset_features_data.csv", "rb"))
    headers = data_reader.next()
    data_list = [row for row in data_reader]

    temp_data_mat = np.array(data_list)
    # We need to convert categorical data to ints/floats so we can use one hot encoding
    data_mat = []
    for (index, col) in enumerate(temp_data_mat.T):
        if(index in [11,12,13,14]):
            le = preprocessing.LabelEncoder()
            le.fit(col)
            #print (list(le.classes_))
            col = le.transform(col)
        elif(index in [3,4,5,6,7,8,9,10]):
            col = preprocessing.scale(col.astype(float))
            #print col
        data_mat.append(col)

    # convert out of the column format
    data_mat = np.array(data_mat).T

    #np.savetxt("tranformed_data.csv", data_mat, delimiter=",", fmt="%s")


    # Imputer converts missing values (?'s) to the mean of the column
    #   mean, median, and mode are available options for strategy
    imp = preprocessing.Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
    data_mat = imp.fit_transform(data_mat)

    # OneHotEncode categorical features so we can use them in NNs
    categorical_feats = [0,1,2,11,12,13,14]
    encoder = preprocessing.OneHotEncoder(categorical_features=categorical_feats, sparse=False)
    data_mat = encoder.fit_transform(data_mat)


    y = data_mat[:,-1]
    x = data_mat[:,:-1]
    print "y:", y
    print "x:", x
    print "Feature count after encoding:",len(x[0])
    
    # Let's split the data into training, validation, and testing
    rows = len(x)
    kfold = 10 # Assuming 10-fold cross validation for everything
    test_start = int((tenth-1)*rows/kfold)
    test_end = int((tenth)*rows/kfold)
    test_matrix = x[test_start:test_end]
    test_labels = y[test_start:test_end]


    x_left = np.delete(x, [i for i in range(test_start, test_end)], 0)
    y_left = np.delete(y, [i for i in range(test_start, test_end)], 0)

    td_amt = .80 # training data amount - inverse is validation amount
    valid_start = int(len(x_left)*td_amt)

    training_matrix = x_left[:valid_start]
    training_labels = y_left[:valid_start]

    valid_matrix = x_left[valid_start:]
    valid_labels = y_left[valid_start:]


    # Now let's compress the data to a .pkl.gz for logistic_sgd's load_data()
    pickle_array = [[training_matrix, training_labels],
                    [valid_matrix, valid_labels],
                    [test_matrix, test_labels]]
    f = gzip.open("../data/diabetes.pkl.gz", "wb")
    pickle.dump(pickle_array, f)
    f.close()

pickle_data()