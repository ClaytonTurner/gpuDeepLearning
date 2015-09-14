from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.cross_validation import cross_val_score, cross_val_predict
import cPickle
import gzip
import random
import numpy as np
import re
from sklearn.preprocessing import Imputer, OneHotEncoder

print "Using diabetes dataset"
datafile = open("../../data/dataset_diabetes/subset_features_data.csv")
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
sub_set = random.sample(no_readmissions, len(readmissions)) + random.sample(readmissions, len(readmissions))    

temp_data_mat = np.array(sub_set)
# We need to convert categorical data to ints/floats so we can use one hot encoding
data_mat = []
for (index, col) in enumerate(temp_data_mat.T):
    unique_vals = []
    for (ii, item) in enumerate(col):
        if item not in unique_vals:
            unique_vals.append(item)
        
        if item == "?":
            col[ii] = "NaN"
        elif not re.match("^\d+",item):
            col[ii] = unique_vals.index(item)  
    data_mat.append(col)

# convert out of the column format
data_mat = np.array(data_mat).T

# Imputer converts missing values (?'s) to the mean of the column
#   mean, median, and mode are available options for strategy
imp = Imputer(missing_values="NaN", strategy="mean", axis=0, copy=False)
data_mat = imp.fit_transform(data_mat)

np.random.shuffle(data_mat)

y = data_mat[:,-1]
x = data_mat[:,:-1]
print "Feature count after encoding:",len(x[0]),"\n"

kfold = 10
subsampleSize = (len(x)/kfold)

treeDepth = 3
print 'deep', treeDepth
overallAccuracySum = 0
readmitedAccuracySum = 0
clf = DecisionTreeClassifier(max_depth=treeDepth)
#cross validation
for fold in range(kfold):
	# Let's split the data into training and testing
	test_start = fold * subsampleSize
	test_end = test_start + subsampleSize
	X_test = x[test_start:test_end]
	Y_test = y[test_start:test_end]
	X_train = np.delete(x, [i for i in range(test_start, test_end)], 0)
	Y_train = np.delete(y, [i for i in range(test_start, test_end)], 0)
	#export_graphviz(clf, out_file='tree.dot', max_depth=8, feature_names=headers)

	clf = clf.fit(X_train, Y_train)
	predictions = clf.predict(X_test)
	correct = 0
	correctYes = 0
	realYes = 0
	for (index, p) in enumerate(predictions):
		#0-no readmited   1-readmited
		if(Y_test[index]==p):
			correct += 1
		if(Y_test[index]==1):
			realYes += 1
			if(p==1):
				correctYes += 1
	overallAccuracy = float(correct)/len(X_test)
	readmitedAccuracy = float(correctYes)/realYes
	overallAccuracySum += overallAccuracy
	readmitedAccuracySum += readmitedAccuracy
	# print "Fold", fold
	# print "Overall accuracy:", overallAccuracy, "---", correct, "of", len(X_test), "pacients"
	# print "Readmited accuracy:", readmitedAccuracy, "---",correctYes, "of", realYes, "pacients\n"

print "Cross Validation", kfold, "folds"
print "Overall accuracy:", overallAccuracySum/kfold
print "Readmited accuracy:", readmitedAccuracySum/kfold, '\n'












# f = gzip.open("diabetes.pkl.gz", 'rb')
# train_set, test_set = cPickle.load(f)
# f.close()
# X = train_set[0]
# Y =  train_set[1]