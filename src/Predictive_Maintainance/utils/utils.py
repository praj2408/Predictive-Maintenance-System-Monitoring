
import pandas as pd

# creating type of failure column
def type_of_failure(row_name,df):
    if df.loc[row_name, 'TWF'] == 1:
        df.loc[row_name, 'type_of_failure'] = 'TWF'
    elif df.loc[row_name, 'HDF'] == 1:
        df.loc[row_name, 'type_of_failure'] = 'HDF'
    elif df.loc[row_name, 'PWF'] == 1:
        df.loc[row_name, 'type_of_failure'] = 'PWF'
    elif df.loc[row_name, 'OSF'] == 1:
        df.loc[row_name, 'type_of_failure'] = 'OSF'
    elif df.loc[row_name, 'RNF'] == 1:
        df.loc[row_name, 'type_of_failure'] = 'RNF'
    else:
        df.loc[row_name, 'type_of_failure'] = 'no failure'
