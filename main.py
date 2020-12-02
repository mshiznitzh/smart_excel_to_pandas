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
import md5
import os_tools
import padas_tools

def Check_for_file_date(filename, date=DT.datetime.today().date()):
    """"""
    timestamp = DT.datetime.fromtimestamp(Path(filename).stat().st_mtime)
    if date != timestamp.date():
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title=' '.join(['Select file for', filename]))
    return filename
def filename_to_feather(filename):
    # TODO add the rest of the supported excel formats
    filename = filename.str.replace('.xlsx', '.feather')
    filename = filename.str.replace('.xlsm', '.feather')
    return filename

def Excel_to_Pandas(dbfilename, dbpath ,Data_path ,filename, CheckforUpdate=None, date=None, sheet=None):
    """
    returns tuple
     """
    logger.info('importing file ' + filename)

    dbfilename = 'check_sum_database.db'
    dbpath = './Excel_to_Pandas_database'
    Data_path = './Data'
    feather_path = './Feather/'
    dbconn = create_connection(dbfilename, dbpath)

    os_tools.Change_Working_Path(Data_path)

    if CheckforUpdate == True:
        Check_for_file_date(filename, date)

    if os.path.exists(filename):
        checksum = md5(filename)
        record = select_file_by_checksum(dbconn, checksum)

    if ~record = None:
        filename = filename_to_feather(filename)

        try
            df = pd.read_feather(str.join(feather_path, filename), columns=None, use_threads=True)
        except:
            logger.error("Error importing file " + filename, exc_info=True)
    else
        try:
            df = pd.read_excel(filename, sheet_name=sheet)
            df.to_feather(str.join(feather_path, filename_to_feather(filename),'_',sheet))

        except:
            logger.error("Error importing file " + filename, exc_info=True)

    if dbconn:
        dbconn.close()
    df = padas_tools.Cleanup_Dataframe(df)

    return filename, df, sheet



if __name__ == "__main__":
    """ This is executed when run from the command line """
    # Setup Logging
    logger = logging.getLogger('root')
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)

    main(filename, check_update=False)