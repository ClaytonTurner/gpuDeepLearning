import sys 

if(len(sys.argv) <= 1):
	print >> sys.stderr, "Proper usage of crossValMean.py: crossValMean.py <algorithm>"
	sys.exit(1)


with open("../results/testPerf" + sys.argv[1] + ".txt", "r") as perf_file:
	datalines = perf_file.readlines()
	accuracySum = 0
	for index in range(10):
		accuracySum += float(datalines[index])
	print accuracySum/10.