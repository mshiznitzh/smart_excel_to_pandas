import sqlite3
from sqlite3 import Error
import OStools.OStools

def create_connection(db_file, dbpath):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    create_table_sql = '''
    CREATE TABLE [IF NOT EXISTS] [schema_name].table_name (
	id data_type PRIMARY KEY,
   	filename data_type varchar,
	checksum data_type varchar,
	table_constraints
    ) [WITHOUT ROWID];
    '''

    if OStools.OStools.check_for_path(dbpath):
        OStools.OStools.Change_Working_Path(dbpath)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    create_table(create_table_sql)


    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_file_data(conn, filename, checksum):
    #TODO Write this function
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project
                )
    conn.commit()
    return cur.lastrowid

def update_file_data(conn, task):
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
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE checksum=?", (checksum,))

    rows = cur.fetchall()

    return rows

def delete_file(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
