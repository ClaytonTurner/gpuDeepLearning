from sklearn.naive_bayes import GaussianNB
import cPickle
import gzip
import random
import numpy as np
import re
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn import preprocessing
from sklearn.metrics import recall_score, accuracy_score


print "Using diabetes dataset"
datafile = open("../data/dataset_diabetes/subset_features_data.csv")
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


# Imputer converts missing values (?'s) to the mean of the column
#   mean, median, and mode are available options for strategy
imp = preprocessing.Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
data_mat = imp.fit_transform(data_mat)

# OneHotEncode categorical features so we can use them in NNs
categorical_feats = [0,1,2,11,12,13,14]
encoder = preprocessing.OneHotEncoder(categorical_features=categorical_feats, sparse=False)
data_mat = encoder.fit_transform(data_mat)

np.random.shuffle(data_mat)

y = data_mat[:,-1]
x = data_mat[:,:-1]
print "y:", y
print "x:", x
print "Feature count after encoding:",len(x[0])

kfold = 10
gnb = GaussianNB()

accuracyList = cross_val_score(gnb, x, y, cv=kfold, scoring='accuracy')
accuracy = sum(accuracyList)/ len(accuracyList)

recallList = cross_val_score(gnb, x, y, cv=kfold, scoring='recall')
recall = sum(recallList)/ len(recallList)

print "Cross Validation", kfold, "folds"
print "Overall accuracy:", accuracy
print "Readmited accuracy:", recall, '\n'






