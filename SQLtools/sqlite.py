import sqlite3
from sqlite3 import Error
import OStools.OStools
import logging
import os

#Setup Logging for Module
logger = logging.getLogger(__name__)

def create_connection(db_file, dbpath):
    logger.info('Started Function')
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS Files (
	id INEGER PRIMARY KEY,
   	filename data_type varchar,
	checksum data_type varchar,
	sheet data_type varchar,
	table_constraints
    )
    '''

    oldpath = os.getcwd()
    OStools.OStools.check_for_path(dbpath)
    OStools.OStools.Change_Working_Path(dbpath)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_table(conn, create_table_sql)
    except Error as e:
        print(e)

    OStools.OStools.Change_Working_Path(oldpath)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    logger.info('Started Function')
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_file_data(conn, filename, checksum, sheet=None):
    logger.info('Started Function')
    #TODO Write this function
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO Files(filename, checksum, sheet)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (filename, checksum, sheet,))
    conn.commit()
    return cur.lastrowid

def update_file_data(conn, task):
    logger.info('Started Function')
    #TODO Write this function
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def select_file_by_checksum(conn, checksum):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    logger.info('Started Function')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Files WHERE checksum=?", (checksum,))

    rows = cur.fetchall()

    return rows

def delete_file(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    logger.info('Started Function')
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
