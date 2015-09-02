import csv

original_diab_data = csv.reader(open("original_diabetic_data.csv","rb"))
formatted_diab_data = csv.writer(open("formatted_diabetic_data.csv", "wb"))

for (index, row) in enumerate(original_diab_data):
    row = [row[j] for j in [6,7,8,9,12,13,14,15,16,17,21,22,24,33,41,49]]
    if(index != 0):
        row[-1] = 'Yes' if row[-1] == '<30' else 'NO'
    formatted_diab_data.writerow(row)
