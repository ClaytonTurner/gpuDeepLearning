import csv


original_diab_data = csv.reader(open("original_data.csv","rb"))
formatted_diab_data = csv.writer(open("subset_features_data.csv", "wb"))
#feature index 1 is patient_nbr
#feature index 7 is discharge_disposition

patientEncounters = {}
addedRows = 0

for (index, row) in enumerate(original_diab_data):
	addRow = True
	if(index>0):
		if(row[1] in patientEncounters):
		#a encounter for this patient was already added
			addRow = False
			patientEncounters[row[1]] += 1
		else:
			patientEncounters[row[1]] = 1

		if(addRow and int(row[7]) in [13,14,19,20,21]):
		#patient was sent to a hospice or died
			addRow = False
	
	if(addRow):
		row = [row[j] for j in [6,7,8,9,12,13,14,15,16,17,21,22,24,33,41,49]]
		addedRows += 1
		formatted_diab_data.writerow(row)

print addedRows
repitedEncounters = {k:v for (k,v) in patientEncounters.items() if(v>1)}
print len(repitedEncounters)