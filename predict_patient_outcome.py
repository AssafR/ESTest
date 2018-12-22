import pandas as pd

def read_from_csv(csvfile):
    """ Read from csv file and convert all values in scientific format to integer"""
    df = pd.read_csv(csvfile,header=None,names=['feature1','feature2','feature3','feature4','feature5','feature6','outcome'])
    return df
pd.set_option('display.expand_frame_repr', False)


csvFile = 'ES_DS_test_section1.csv'
df = read_from_csv(csvFile)
df = df.astype({'outcome':int})
print(df.describe())