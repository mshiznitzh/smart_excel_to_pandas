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
import Hashtools.md5
import OStools.OStools
import PandasTools.PandasTools
import pandas as pd
import SQLtools.sqlite

#Setup Logging for Module
logger = logging.getLogger(__name__)

def Convert_df_to_feather(df , filename):
    filename = PandasTools.PandasTools.filename_to_feather("./"+filename)
    df.to_feather(filename)

def Smart_Excel_to_Pandas(filename, sheet = 0, dbfilename = 'check_sum_database.db', dbpath = './Excel_to_Pandas_database' ,Data_path = '../Data', feather_path = './Feather/'):
    """
    returns tuple
     """
    logger.info('importing file ' + filename)

    OStools.OStools.check_for_path(feather_path)


    dbconn = SQLtools.sqlite.create_connection(dbfilename, dbpath)

    OStools.OStools.Change_Working_Path(Data_path)

    #if os.path.exists(filename):
    checksum = Hashtools.md5.md5(filename)
    record = SQLtools.sqlite.select_file_by_checksum(dbconn, checksum)

    if len(record) >> 0:
        if isinstance(sheet, int):
            df = pd.read_feather(feather_path + PandasTools.PandasTools.filename_to_feather(filename))
            df = PandasTools.PandasTools.Cleanup_Column_Headers_Dataframe(df)
        else:
            df = {}
            for item in record:
                try:
                    df.update({item[3]: pd.read_feather(feather_path + item[3] + '_' + PandasTools.PandasTools.filename_to_feather(filename)
                    , columns=None, use_threads=True)})
                    df[x] = PandasTools.PandasTools.Cleanup_Column_Headers_Dataframe(df[x])
                except:
                    logger.error("Error importing file " + filename, exc_info=True)
    else:
        try:
            df = pd.read_excel(filename, sheet_name=sheet)
        except:
            logger.error("Error importing file " + filename, exc_info=True)

        if isinstance(df, dict):
            for x in df:
                try:
                    df[x].columns = df[x].columns.astype(str)
                    df[x].reset_index().to_feather(feather_path + str(x) + '_' + PandasTools.PandasTools.filename_to_feather(filename))

                    df_f = pd.read_feather(feather_path + str(x) + '_' + PandasTools.PandasTools.filename_to_feather(filename))

                    if df[x].reset_index().equals(df_f):
                        SQLtools.sqlite.create_file_data(dbconn, filename, checksum, x)
                    else:
                        logger.info('Feather copy not equal to excel, not adding to database')

                except:
                    print(filename + 'Imports with an error' )
                #df[x] = PandasTools.PandasTools.Cleanup_Dataframe(df[x])

                df[x] = PandasTools.PandasTools.Cleanup_Column_Headers_Dataframe(df[x])
        else:
            try:
                df.columns = df.columns.astype(str)
                df.reset_index().to_feather(
                    feather_path + PandasTools.PandasTools.filename_to_feather(filename))

                df_f = pd.read_feather(
                    feather_path + PandasTools.PandasTools.filename_to_feather(filename))

                if df.reset_index().equals(df_f):
                    SQLtools.sqlite.create_file_data(dbconn, filename, checksum, '0')
                else:
                    logger.info('Feather copy not equal to excel, not adding to database')

            except:
                print(filename + 'Imports with an error')

            df = PandasTools.PandasTools.Cleanup_Column_Headers_Dataframe(df)
    if dbconn:
        dbconn.close()


    return (filename, df)

def read_excel_all():
    logger.info('Started Function')
    for file in OStools.OStools.filesearch('.xlsx'):
        pd.read_excel(file)

def read_feather_all():
    logger.info('Started Function')
    for file in OStools.OStools.filesearch('.feather'):
        df = pd.read_feather(file)

def feather_me():
    logger.info('Started Function')
    for file in OStools.OStools.filesearch('.xlsx'):
        df = pd.read_excel(file)
        Convert_df_to_feather(df, file)

def main():
    logger.info('Started Function')

    dbfilename = 'check_sum_database.db'
    dbpath = './Excel_to_Pandas_database'
    Data_path = '../Data'
    feather_path = './Feather/'

    OStools.OStools.Change_Working_Path(Data_path)

    xlsx_list = OStools.OStools.filesearch('.xlsx')
    for file in xlsx_list:
        Smart_Excel_to_Pandas(file, None,bfilename, dbpath, Data_path, feather_path)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    # Setup Logging
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)

    main()