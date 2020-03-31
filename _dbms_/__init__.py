import os
import sqlite3
from sqlite3 import Error

import _logging_ as _log
import _config_ as _cfg


def sql_connection(dbpath='mydatabase.db'):
    """Returns SQLite3 connection to db created at provided path.

    Args:
        dbpath: Local db path for SQLite3 Database file.

    Returns:
        Local db connection object.
    """
    try:
        _log.logger.debug("creating db at %s" % (dbpath))
        db_connection = sqlite3.connect(dbpath)
        return db_connection
    except Error:
        _log.logger.critical(Error)


def create_schema_messages(db):
    """Creates 'messages' schema on given DB connection.

    Args:
        db: Local db connection object.
    """
    _log.logger.debug("creating table message")
    cursorObj = db.cursor()
    cursorObj.execute("""CREATE TABLE IF NOT EXISTS messages(
        id text,
        threadId text,
        labelIds text,
        sender text,
        receiver text,
        subject text,
        date text,
        snippet text,
        internalDate integer,
        msg blob,
        CONSTRAINT id_pk PRIMARY KEY (id))""")
    cursorObj.execute("""CREATE INDEX IF NOT EXISTS idx_messages_threadId
        ON messages (threadId);""")
    cursorObj.execute("""CREATE INDEX IF NOT EXISTS idx_messages_internalDate
        ON messages (internalDate);""")
    db.commit()


def sender_of_message(message):
    try:
        return [item['value'] for item in message['payload']['headers'] if item['name'] == 'From'][0]
    except:
        return ""


def receiver_of_message(message):
    try:
        return [item['value'] for item in message['payload']['headers'] if item['name'] == 'To'][0]
    except:
        return ""


def subject_of_message(message):
    try:
        return [item['value'] for item in message['payload']['headers'] if item['name'] == 'Subject'][0]
    except:
        return ""


def date_of_message(message):
    try:
        return [item['value'] for item in message['payload']['headers'] if item['name'] == 'Date'][0]
    except:
        return ""


def add_message(db, message):
    """Get and Delete a list of messages from GMail by Query.

    Args:
        db: Local db connection object.
        message: GMail message JSON object as read by get api.
    """
    _log.logger.debug("[+] adding message: %s" % (message['id']))

    cursorObj = db.cursor()
    sql_stmt = """INSERT INTO messages
                        (id, threadId, labelIds, sender, receiver, subject, date, snippet, internalDate, msg)
                        VALUES (?,?,?,?,?,?,?,?,?,?)"""
    values = (
        message['id'],
        message['threadId'],
        ",".join(message['labelIds']),
        sender_of_message(message),
        receiver_of_message(message),
        subject_of_message(message),
        date_of_message(message),
        message['snippet'],
        int(message['internalDate']),
        str(message),
    )

    try:
        cursorObj.execute(sql_stmt, values)
        _log.logger.debug("on %s | from: %s | to: %s | subject: %s" % (
            date_of_message(message),
            sender_of_message(message),
            receiver_of_message(message),
            subject_of_message(message)))
        _log.logger.debug("---------------------")
        db.commit()
    except:
        _log.logger.error("failed to insert for %s" % (message['id']))
        sys.exit(0)


def dbpath_by_year(year):
    """Returns DB path generated based on year.

    Args:
        year: Year for which db path need to be generated.

    Returns:
        DB filesystem path.
    """
    db_name = "gmail-to-delete-%d.db" % (year)
    return os.path.join(_cfg.data_basepath(), db_name)


def connection_by_year(year):
    """Returns SQLite3 connection to db created at path for given year.

    Args:
        year: Year for which db path need to be generated.

    Returns:
        Local db connection object.
    """
    return sql_connection(dbpath_by_year(year))
