import cPickle
import gzip
import random
import numpy as np
import re
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn.preprocessing import Imputer, OneHotEncoder, LabelEncoder
from sklearn.metrics import recall_score, accuracy_score
import csv


print "Using diabetes dataset"
data_reader = csv.reader(open("../data/dataset_diabetes/subset_features_data.csv", "rb"))
headers = data_reader.next()
data_list = [row for row in data_reader]

temp_data_mat = np.array(data_list)
# We need to convert categorical data to ints/floats so we can use one hot encoding
data_mat = []
for col in temp_data_mat.T:
	if(not re.match("^\d+",col[0])):
		le = LabelEncoder()
		col = le.fit_transform(col)
		print (list(le.classes_))
	data_mat.append(col)

# convert out of the column format
data_mat = np.array(data_mat).T

# Imputer converts missing values (?'s) to the mean of the column
#   mean, median, and mode are available options for strategy
imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
data_mat = imp.fit_transform(data_mat)

#np.random.shuffle(data_mat)

y = data_mat[:,-1]
x = data_mat[:,:-1]
print "Feature count after encoding:",len(x[0]),"\n"

kfold = 10
treeDepth = 3
clf = DecisionTreeClassifier(max_depth=treeDepth)

accuracyList = cross_val_score(clf, x, y, cv=kfold, scoring='accuracy')
accuracy = sum(accuracyList)/ len(accuracyList)

recallList = cross_val_score(clf, x, y, cv=kfold, scoring='recall')
recall = sum(recallList)/ len(recallList)

print 'Tree max depth', treeDepth
print "Cross Validation", kfold, "folds"
print "Overall accuracy:", accuracy
print "Readmited accuracy:", recall, '\n'







