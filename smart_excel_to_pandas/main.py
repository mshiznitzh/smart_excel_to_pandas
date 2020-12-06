"""
This module will take a list of tuple that contains filename, dataframe name and check for update. It will then unpack
the tuples. Cacultate the checksum of each file. Check if the check sum matches the last imported file.
If it does then the dataframe will be imported via the prevous exported feather format.

If not then a checksum of the file will be cacultated and saved to the sqllite database. File imported to a dataframe
and exported to a feather format for future reads.

After all dataframes have been imported each dataframe will be added to the tuple

Retruns tuple that was imported with dataframes
"""

#TODO: Update Docstring

__author__ = "Mike Howard"
__version__ = "0.1.0"
__license__ = "MIT"

import logging
import os.path
from Hashtools import md5
import OStools.OStools
import PandasTools.PandasTools
import timeit
import pandas as pd

def Convert_df_to_feather(df , filename):
    filename = PandasTools.PandasTools.filename_to_feather(filename)
    df.to_feather(filename)

def Excel_to_Pandas(dbfilename, dbpath ,Data_path ,filename, CheckforUpdate=None, date=None, sheet=None):
    """
    returns tuple
     """
    logger.info('importing file ' + filename)

    dbfilename = 'check_sum_database.db'
    dbpath = './Excel_to_Pandas_database'
    Data_path = '../Data'
    feather_path = './Feather/'
    dbconn = create_connection(dbfilename, dbpath)

    OStools.Change_Working_Path(Data_path)

    if CheckforUpdate == True:
        Check_for_file_date(filename, date)

    if os.path.exists(filename):
        checksum = md5(filename)
        record = select_file_by_checksum(dbconn, checksum)

    if ~record == None:
        filename = filename_to_feather(filename)

        try:
            df = pd.read_feather(str.join(feather_path, filename), columns=None, use_threads=True)
        except:
            logger.error("Error importing file " + filename, exc_info=True)
    else:
        try:
            df = pd.read_excel(filename, sheet_name=sheet)
            df.to_feather(str.join(feather_path, filename_to_feather(filename),'_',sheet))

        except:
            logger.error("Error importing file " + filename, exc_info=True)

    if dbconn:
        dbconn.close()
    df = PandasTools.Cleanup_Dataframe(df)

    return filename, df, sheet

def read_excel_all(list):
    for file in list:
        pd.read_excel(file)

def read_feather_all(list):
    for file in list:
        df = pd.read_excel(file)

def feather_me(list):
    for file in list:
        df = pd.read_excel(file)
        Convert_df_to_feather(df, file)

def main():
    OStools.OStools.Change_Working_Path('../Data')
    #get all xlsx files in folder
    xlsx_list = OStools.OStools.filesearch('.xlsx')


    #Time how long it takes to import all sheets
    read_excel_all(xlsx_list)
    feather_list = feather_me(xlsx_list)
    read_feather_all(feather_list)
    feather_list = OStools.OStools.filesearch('.feather')
    #export to feather
    # Time how long it takes to import all sheets via feather

if __name__ == "__main__":
    """ This is executed when run from the command line """
    # Setup Logging
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)

    main()