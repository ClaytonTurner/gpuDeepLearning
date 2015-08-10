library(AUC)

alg_labels = "DBN/labels.txt"
alg_p_values = "DBN/p_values.txt"

labels <- read.csv(alg_labels,sep="\n",header=F)
predprobs <- read.csv(alg_p_values,sep="\n",header=F)

labels <- factor(round(labels[,1]))
predprobs <- predprobs[,1]

print("Accuracy")
sum(round(predprobs) == labels)/length(labels)

print("AUC")
auc(roc(predprobs,labels))
