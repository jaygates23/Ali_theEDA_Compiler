import pandas as pd 
import numpy as np 
import warnings
import os
import argparse
import pandas_read_xml as pdx 
from datetime import datetime 
from io import StringIO
import glob
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import t


class CommandLine:
    def _init_(self):
        msg = "Adding description"
        parser =  argparse.ArgumentParser(description = msg)
        parser.add_argument("-i", "--InputFile", action = 'store', help = "Pass input file")
        parser.add_argument("-o", "--Output", action = 'store', help = "Create Output File")
        parser.add_argument("-KeyColumns", "--colName1", action = 'store', help = "Choose Columns to make Unique")
        parser.add_argument("-expandFactor", "--n", action = 'store', help = "n Must be greater than 1")
        args = parser.parse_args()
        status = False

        if args.InputFile:
            args.InputFile = read_file( args.InputFile)
            status = True
        #if args.Output:
        #    args.Output = 
        if not status:
            pass


def get_dataFile(filename):
    while True:
        try:
            file = open(filename, 'r', encoding= "utf8")
        except FileNotFoundError:
            print(input("Please enter Input Filename, error finding file:"))
            continue
        else:
            break

    return file, filename


def get_folder():
    #/Users/tjscott/Documents/GitHub/eCommerceBehavior/Data_files
    path = input("Please enter Input folder name:")
    ext = input("Please enter type of Files to include:")
    ext = "*."+ ext
    #path =  # use your path
    #all_files = glob.glob(path + "/*.csv")
    all_files = glob.glob(os.path.join(path, "*.csv")) #make list of paths
    col= ['event_time', 'event_type', 'product_id', 'category_id',
      'category_code', 'brand', 'price', 'user_id', 'user_session']
    
    dict={}
    for file in all_files:
        # Getting the file name without extension
        file_name = os.path.splitext(os.path.basename(file))[0]
        data = pd.read_csv(file, names=col, header=0, low_memory=False )
        dict.update({file_name: data })

    return dict 

"""Create File or Folder marker"""
def get_uniqueCols(col_name):
    while True:
        try:
            col_name = col_name.split(",")
            col_name = [x.strip(' ') for x in col_name]
        except (RuntimeError, TypeError, NameError):
            print(input("Please re-enter Unique column name:"))
            continue
        else:
            break
    return col_name

def fill_cols( df, col_name, size_increase):
    uni_cols = get_uniqueCols(col_name)
    df2 = multiplier(df, size_increase)
    cols = list(df2.columns)
    st_loc = df.tail(1).index[0]
    end_loc = df2.tail(1).index[0]

    for col in cols:
        if col in uni_cols:
            type = castCol(df, col)
            if type == 'object':
                entry = df[col].iloc[-1]
                entry = entry.split("-")
                entry1 = entry[0]
                entry2 = int(entry[-1])

                for i in df2.index:
                    if i > st_loc:
                        warnings. filterwarnings("ignore")
                        entry3 = entry2+1
                        entry2 = entry3
                        entry = entry1 + '-' + str(entry3)
                        df2[col][i] = entry
            else:
                max = df[col].max()
                for i in df2.index:
                    if i > st_loc:
                        warnings. filterwarnings("ignore")
                        entry = max+1
                        max = entry
                        df2[col][i] = entry

        else:
            df2[col] = df2[col].replace({0:df2[col][0]})
    
    return df2
def castCol(df, col):
    datatypes = df.dtypes[col]
    return datatypes

def multiplier(df1, size_increase):

    end_loc = df1.iloc[:,1]
    end_loc = end_loc.size 
    cols = list(df1.columns)
    size_increase = (size_increase * end_loc)
    df2 = pd.concat([df1, pd.DataFrame(0, columns = cols,
                                       index = range(size_increase))],
                                       ignore_index= True)
    
    return df2

def get_filetype(file):
    type = os.path.splitext(os.path.basename(file))[1]
    return type

def read_file( filename):
    file, filename = get_dataFile(filename)
    type = get_filetype(filename)
    dat = '.dat'
    csv = '.csv'
    xml = '.xml'
    json = '.json'

    if type == dat:
        df = pd.read_csv(file, encoding = 'ISO-8859-1', delimiter = ',')
    elif type == csv:
        df = pd.read_csv(file, encoding = 'ISO-8859-1', delimiter = ',')
    
    elif type == xml:
        df = pdx.read_xml()
    
    elif type == json:
        df = read_json()

    return df

def createTar( df, filename):
    records, cols_num = df.shape
    name = get_filename(filename)
    businessDate = datetime.today().strftime('%Y-%m-%d')
    size = get_size(filename)
    data = [{'FILENAME': name, 'BusinessDate': businessDate, 
             'NoOfRecords': records, 'FileSize': size}]
    outputFilename = name + ".trg"
    tar = pd.DataFrame(data)
    file = tar.to_csv(outputFilename, index= False, sep = ',')
    return tar

def get_filename(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    
    return name

def get_size(file):
    try:
        file_size = os.path.getsize(file)
    
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("OS error occurred.")
    
    return file_size

def createOutput( df, outputFilename):
    file = df.to_csv(outputFilename, index= False, sep = ',')

    return file

def stats_Create():
    return

def linearAlgebra():
    return

def auto_ML():
    return

def feature_Engineering():
    return

def get_delimiter():
    return


def find_relationships():
    results = {}
    x1=x.copy().select_dtypes(include=['object']).drop(['A16'], axis=1)
    for column in x1:
        observed = pd.crosstab(x['A16'], x1[column])
        observed = observed.values
        chi2, pvalue, dof, expected = stats.chi2_contingency(observed)
    if pvalue < .05:
      results.setdefault(column, [chi2, pvalue])
    return(results)
    

def confidence_interval():
    """
  Calculate a confidence interval around a sample mean for given data.
  Using t-distribution and two-tailed test, default 95% confidence. 
  
  Arguments:
    data - iterable (list or numpy array) of sample observations
    confidence - level of confidence for the interval
  
  Returns:
    tuple of (mean, lower bound, upper bound)
  """
    data = np.array(data)
    mean = np.mean(data)
    n = len(data)
  # pass extra parameter (ddof=1) to calculate **sample** standard deviation
    s = data.std(ddof=1)
    stderr = s / np.sqrt(n)
  # Lookup the t-statistic that corresponds to 95% area under the curve
  # for my given degrees of freedom: 49
    t = stats.t.ppf((1 + confidence) / 2.0, n - 1)
    margin_of_error = t*stderr
    return (mean, mean - margin_of_error, mean + margin_of_error)
    

def find_usable_data():
    return

def create_graphs():
    return


    




def main():
    #app = CommandLine()
    #print("Hello World")
    filename = input("Please enter Input Filename:")
    outputFilename =  input("Please Enter Output file name:")
    col_name = input("Please Enter Unique column name(s):")
    size_increase = int(input("Please Set Multiplier:"))
    df = read_file(filename)
    df4 = fill_cols( df, col_name, size_increase)
    file = df4.to_csv(outputFilename, index=False, sep =',')
    file2 = createTar(df4, outputFilename)


if __name__ == "__main__":
    main()


