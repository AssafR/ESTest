import json
from decimal import Decimal
from pprint import pprint
import csv
import glob


glob.glob('./*.txt')

section2DataDir = "./section2Data/"
filename = "./section2Data/entryNum_0"
jsonFile = filename + ".json"
csvFile = filename + ".csv"

def find_files_in_dir_with_extension(directory,extension):
    return glob.glob(directory + "/*." + extension)

def retrive_only_filenames(full_names):


def read_json_file(jsonFile):
    with open(jsonFile) as data_file:
        dataJson = json.load(data_file)
        return dataJson

def read_from_csv_to_float_array(csvFile):
    with open(csvFile) as data_file:
        reader = csv.reader(data_file, delimiter=',', quotechar='|')
        dataCsv = [float(element) for sublist in reader for element in sublist]
        return dataCsv

print(find_files_in_dir_with_extension(section2DataDir,"csv"))