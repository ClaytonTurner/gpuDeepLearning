from sklearn.naive_bayes import GaussianNB
import cPickle
import gzip

f = gzip.open("diabetes.pkl.gz", 'rb')
train_set, test_set = cPickle.load(f)
f.close()
X = train_set[0]
Y =  train_set[1]

gnb = GaussianNB()
y_pred = gnb.fit(X, Y).predict(test_set[0])

correct = 0
correctYes = 0
realYes = 0
for (index, p) in enumerate(y_pred):
	if(test_set[1][index]==p==1):
		correctYes +=1
	if(test_set[1][index]==1):
		realYes +=1
	if(p==test_set[1][index]):
		correct += 1.

print correct / len(test_set[0]), "---", correct
print "accuracy ", float(correctYes) / realYes, "----", correctYes
print "Readmited ", realYes, " pacients out of ", len(test_set[0])
print "Not readmited percentege", float(len(test_set[0])-realYes)/len(test_set[0])
