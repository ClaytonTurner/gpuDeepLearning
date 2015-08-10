import csv

diabetes_data = csv.reader(open("../data/dataset_diabetes/diabetic_data.csv","rb"))
diabetes_2outs_file = csv.writer(open("../data/dataset_diabetes/diabetic_data_2outs.csv", "wb"))

for (index, row) in enumerate(diabetes_data):
    if(index != 0):
        row[-1] = '<30' if row[-1] == '<30' else 'NO'
    diabetes_2outs_file.writerow(row)
