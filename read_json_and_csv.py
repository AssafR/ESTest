import json
import csv
import glob
from pprint import pprint
import pandas as pd

section2DataDir = "./section2Data/"
json_columns = ['ID', 'Code']
csv_columns = ['ID', 'weight', 'height', 'age']
output_csv = "combined.csv"


def find_files_in_dir_with_extension(directory, extension):
    return glob.glob(directory + "/*." + extension)


def read_json_file(jsonFile):
    with open(jsonFile) as data_file:
        json_dict = json.load(data_file)
        json_dict['Code'] = int(json_dict['Code'])
        json_dict['ID'] = int(json_dict['ID'])
        return json_dict


def read_from_csv_to_int_array(csvfile):
    """ Read from csv file and convert all values in scientific format to integer"""
    with open(csvfile) as data_file:
        reader = csv.reader(data_file, delimiter=',', quotechar='|')
        return [int(float(element)) for sublist in reader for element in sublist]


def add_dicts_to_df(df, dicts, index):
    """Given data stored as a list of dictionaries with keys corresponding to dataframe columns,
    add the values as rows to the dataframe
    """
    for dictionary in dicts:
        new_df = pd.DataFrame.from_records([dictionary])
        new_df.set_index(index, inplace=True)
        df = df.append(new_df)
    return df


def patients_by_code_older(df, code, age_older_than):
    df_filtered = df.loc[(df['age'] > age_older_than) & (df['Code'] == code)]
    return df_filtered


def print_patients_by_code_older(df, code, age_older_than):
    patients = patients_by_code_older(df, code, age_older_than)
    print("Number of patients:", patients.shape[0])
    print("Patient data:")
    print(patients)


# Data preparation
df_jsn = pd.DataFrame(columns=json_columns)
df_jsn.set_index('ID', inplace=True)
df_csv = pd.DataFrame(columns=csv_columns)
df_csv.set_index('ID', inplace=True)

# Data read from files
jsonDictsFromFiles = [read_json_file(jsonFile) for jsonFile in
                      find_files_in_dir_with_extension(section2DataDir, "json")]
csvDictsFromFiles = [dict(zip(csv_columns, read_from_csv_to_int_array(csvFile)))
                     for csvFile in find_files_in_dir_with_extension(section2DataDir, "csv")]

# Data saved to Pandas dataframes
df_jsn = add_dicts_to_df(df_jsn, jsonDictsFromFiles, 'ID')
df_csv = add_dicts_to_df(df_csv, csvDictsFromFiles, 'ID')
df_combined = df_csv.join(df_jsn, on='ID')  # Joined data by ID

# Calculations on the data

csv_mean = df_csv.mean(axis=0)  # Calculate mean of all columns. Result Type: Series
print("*** Mean values for population ***")
for column, value in csv_mean.iteritems():
    print(column, ":", value)

# Drop all rows where "Code" or "age" do not exist
df_legal_code_age = df_combined.dropna(axis='index', subset=['Code', 'age'])
print_patients_by_code_older(df_legal_code_age, 597, 20)
print_patients_by_code_older(df_legal_code_age, 597, 50)
print_patients_by_code_older(df_legal_code_age, 530, 20)

# Create and write the full data with no missing values allowed
df_combined_nonan = df_combined.dropna(axis='index')
df_combined_nonan.to_csv(output_csv)
