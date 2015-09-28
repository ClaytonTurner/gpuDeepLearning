# This file is a interface to handle the database
#WARNING: the features 'diag_1', 'diag_2' and 'diag_3' should not be included in any analyze without huge attention because they are a mix of numbers and strings
#PS:'encounter_id' and 'patient_nbr' are not take into account for the functions below. If you decide by a reason that only God knows using them, you have to change features_to_encode and features_to_scale

features = ['encounter_id', 'patient_nbr', 'race', 'gender', 'age',	'weight', 'admission_type_id', 'discharge_disposition_id', 'admission_source_id', 'time_in_hospital', 'payer_code', 'medical_specialty', 'num_lab_procedures', 'num_procedures', 'num_medications', 'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses', 'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted']
features_to_scale = ['time_in_hospital', 'num_lab_procedures', 'num_procedures', 'num_medications', 'number_outpatient', 'number_emergency', 'number_inpatient', 'number_diagnoses']
features_to_encode = ['race', 'gender', 'age', 'weight', 'payer_code', 'medical_specialty', 'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone', 'change', 'diabetesMed']
features_to_hot_encode = features_to_encode + ['admission_type_id', 'discharge_disposition_id', 'admission_source_id']


#'sub_set_features' must follow the same order of the list 'features'
sub_set_features = ['admission_type_id', 'discharge_disposition_id', 'admission_source_id', 'time_in_hospital', 'payer_code', 'medical_specialty', 'num_lab_procedures', 'num_procedures', 'num_medications', 'number_outpatient', 'number_emergency', 'number_inpatient', 'number_diagnoses', 'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted']
#left_out_features = ['encounter_id', 'patient_nbr', 'race', 'gender', 'age', 'weight', 'diag_1', 'diag_2', 'diag_3']

def get_sub_feature_indexes():
	return [index for (index, f) in enumerate(features) if f in sub_set_features]

def get_left_out_feature_indexes():
	return [index for (index, f) in enumerate(features) if f not in sub_set_features]

def get_indexes_to_scale():
	return [index for (index, f) in enumerate(sub_set_features) if f in features_to_scale]

def get_indexes_to_encode():
	return [index for (index, f) in enumerate(sub_set_features) if f in features_to_encode]

def get_indexes_to_hot_encode():
	return [index for (index, f) in enumerate(sub_set_features) if f in features_to_hot_encode]
