from sklearn import tree
import cPickle
import gzip

f = gzip.open("diabetes.pkl.gz", 'rb')
train_set, test_set = cPickle.load(f)
f.close()
X = train_set[0]
Y =  train_set[1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
print clf.score(test_set[0], test_set[1])
predictions = clf.predict(test_set[0])

correct = 0
correctYes = 0
realYes = 0
for (index, p) in enumerate(predictions):
	if(test_set[1][index]==p==1):
		correctYes +=1
	if(test_set[1][index] == 1):
		realYes +=1
	if(p == test_set[1][index]):
		correct += 1

print "Overall accuracy:", float(correct)/len(test_set[0]), "---", correct, "of", len(test_set[0]), "pacients"
print "Readmited accuracy:", float(correctYes)/realYes, "---",correctYes, "of", realYes, "pacients"