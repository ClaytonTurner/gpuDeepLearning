import csv
import random
import DatabaseManager

# sub_set_features = [6,7,8,9,12,13,14,15,16,17,21,22,24,33,41,49]
sub_set_indexes = DatabaseManager.get_sub_feature_indexes()

data_reader = csv.reader(open("original_data.csv","rb"))
data_writer = csv.writer(open("subset_features_data.csv", "wb"))

header = data_reader.next()
header = [header[j] for j in sub_set_indexes]
data_writer.writerow(header)

patientEncounters = {}
readmitted = []
no_readmitted = []

for (index, row) in enumerate(data_reader):
	addRow = True

	if(row[1] in patientEncounters):
	#feature index 1 is patient_nbr
	#a encounter for this patient was already added
		addRow = False
		patientEncounters[row[1]] += 1
	else:
		patientEncounters[row[1]] = 1

	if(addRow and int(row[7]) in [13,14,19,20,21]):
	#feature index 7 is discharge_disposition
	#patient was sent to a hospice or died
		addRow = False
	
	if(addRow):
		row = [row[j] for j in sub_set_indexes]
		if(row[-1]=='Yes'):
			row[-1] = 1
			readmitted.append(row)
		else:
			row[-1] = 0
			no_readmitted.append(row)

print 'number of readmissions:', len(readmitted)
sub_set = random.sample(no_readmitted, len(readmitted)) + readmitted
random.shuffle(sub_set)
data_writer.writerows(sub_set)


repitedEncounters = {k:v for (k,v) in patientEncounters.items() if(v>1)}
print len(repitedEncounters)

print DatabaseManager.get_sub_feature_indexes()
print DatabaseManager.get_left_out_feature_indexes()
print DatabaseManager.get_indexes_to_scale()
print DatabaseManager.get_indexes_to_encode()
print DatabaseManager.get_indexes_to_hot_encode()