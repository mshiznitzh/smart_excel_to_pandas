''''''

import logging
import datetime as DT
import tkinter as tk

#Setup Logging for Module
logger = logging.getLogger(__name__)

def Excel_to_Pandas(filename,check_update=False):
    logger.info('importing file ' + filename)
    df=[]
    if check_update == True:
        timestamp = DT.datetime.fromtimestamp(Path(filename).stat().st_mtime)
        if DT.datetime.today().date() != timestamp.date():
            root = tk.Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(title =' '.join(['Select file for', filename]))

    try:
        df = pd.read_excel(filename, sheet_name=None)
        df = pd.concat(df, axis=0, ignore_index=True)
    except:
        logger.error("Error importing file " + filename, exc_info=True)

    df=Cleanup_Dataframe(df)
    logger.debug(df.info(verbose=True))
    return df

def Cleanup_Column_Headers_Dataframe(df):
    logger.info('Started Function')
    print('Cleanup_Column_Headers_Dataframe started')
    # Remove whitespace on both ends of column headers
    df.columns = df.columns.str.strip()

    # Replace whitespace in column header with _
    df.columns = df.columns.str.replace(' ', '_')

    return df

def filename_to_feather(filename):
    # TODO add the rest of the supported excel formats
    logger.info('Started Function with filename: ' + filename)
    filename = filename.replace('.xlsx', '.feather')
    filename = filename.replace('.xlsm', '.feather')
    logger.info('Function returning filename: ' + filename)
    return filename
