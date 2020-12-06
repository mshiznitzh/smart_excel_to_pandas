'''This module is home to Mike Howard's tools that use the os module'''
import os.path
import datetime as DT
import logging
import glob
import sys

#Setup Logging for Module
logger = logging.getLogger(__name__)

def check_for_path(path):
    logger.info('Started Function')
    if ~os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            return False
    return True

def filesearch(word=""):
    """Returns a list with all files with the word/extension in it"""
    logger.info('Starting filesearch')
    file = []
    for f in glob.glob("*"):
        if word[0] == ".":
            if f.endswith(word):
                file.append(f)

        elif word in f:
            file.append(f)
            #return file
    logger.debug(file)
    return file

def Change_Working_Path(path):
    logger.info('Started Function')
    # Check if New path exists
    #if os.path.exists(path):
        # Change the current working Directory
    try:
        os.chdir(path)  # Change the working directory
    except OSError:
        logger.error("Can't change the Current Working Directory, aborting programing", exc_info = True)
        sys.exit()
    #else:
     #   print("Can't change the Current Working Directory because this path doesn't exits")


def Check_for_file_date(filename, date=DT.datetime.today().date()):
    """"""
    logger.info('Started Function')
    timestamp = DT.datetime.fromtimestamp(Path(filename).stat().st_mtime)
    if date != timestamp.date():
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title=' '.join(['Select file for', filename]))
    return filename


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/