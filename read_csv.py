import pandas as pd
from IPython.display import display


def read_file(path_to_file, excel_flag = False, sheet_name = None, verbosity = 0):
    
    try:
        if(excel_flag == False):
            df = pd.read_csv(path_to_file)
        
        elif(excel_flag == True):
            if(sheet_name == None):
                df = pd.read_excel(path_to_file)
                
            else:
                df = pd.read_excel(path_to_file, sheet_name = sheet_name)
        if(verbosity == 1):
            display(df.head())
            display(df.tail())

    except:
        raise Exception("File Error")
        
    return df

