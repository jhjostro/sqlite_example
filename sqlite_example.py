#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Simple SQLite Example in python.

sqlite_example.py
sqlite_example
(C)2020 Jon Duesterhoeft
jon.duesterhoeft@gmail.com
"""

import sqlite3
from sqlite3 import Error


def connect_to_database(db_file: str) -> sqlite3.Connection:
    """
    Connect to the database file passed as db_file.

    Note that if db_file doesn't already exist, it will be created.

    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as err:
        print(err)

    return conn


def create_table(conn: sqlite3.Connection, create_statement: str) -> None:
    """Create a new database table from string passed as create_statement."""
    try:
        c = conn.cursor()
        c.execute(create_statement)
    except Error as err:
        print(err)

    return None


def main():
    """Run main function."""
    database_file = 'Database.sqlite'  # name of database file.
    conn = connect_to_database(database_file)  # create connection to database.

    if conn is not None:  # make sure conenction is active.
        # create two new database tables.
        new_table_timestamps = ("""CREATE TABLE IF NOT EXISTS timestamps(
            timestampID INTEGER NOT NULL PRIMARY KEY,
            timestamp NUMERIC NOT NULL
            );""")
        new_table_observations = ("""CREATE TABLE IF NOT EXISTS observations(
            observationID INTEGER NOT NULL PRIMARY KEY,
            observationValue REAL NOT NULL,
            timestampID INTEGER NOT NULL,
            FOREIGN KEY (timestampID) REFERENCES timestamps(timestampID)
            );""")
        create_table(conn, new_table_timestamps)
        create_table(conn, new_table_observations)
    else:  # print error if database connection fails.
        print('Error in database connection.')


if __name__ == '__main__':
    main()
