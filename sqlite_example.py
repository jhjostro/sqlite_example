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
        cur = conn.cursor()
        cur.execute(create_statement)
    except Error as err:
        print(err)

    return None


def insert_timestamp(conn: sqlite3.Connection, timestamp_val: str) -> int:
    """
    Insert a new row in timestamps table.

    Pass the timestamp value as timestamp_val, returns id of new row.

    """
    row_statement = str('INSERT INTO timestamps(timestampVal) VALUES ("'
                        + timestamp_val + '")')
    try:
        cur = conn.cursor()
        cur.execute(row_statement)
        conn.commit()
    except Error as err:
        print(err)

    print(type(cur.lastrowid))

    return cur.lastrowid


def insert_observation(conn: sqlite3.Connection, observation_val: str,
                       timestamp_id: int) -> int:
    """
    Insert a new row in observations table, linking to a timestamp.

    Pass the observation value as observation_val and the timestamp row id as
    timestamp_id, returns id of new row in observations.

    """
    row_statement = str('INSERT INTO observations(observationVal, timestampID)'
                        + 'VALUES ("' + observation_val + '",'
                        + str(timestamp_id) + ')')
    try:
        cur = conn.cursor()
        cur.execute(row_statement)
        conn.commit()
    except Error as err:
        print(err)

    print(type(cur.lastrowid))

    return cur.lastrowid


def main():
    """Run main function."""
    database_file = 'Database.sqlite'  # name of database file.
    conn = connect_to_database(database_file)  # create connection to database.

    if conn is not None:  # make sure conenction is active.
        # create two new database tables.
        new_table_timestamps = ("""CREATE TABLE IF NOT EXISTS timestamps(
            timestampID INTEGER NOT NULL PRIMARY KEY,
            timestampVal NUMERIC NOT NULL
            );""")
        new_table_observations = ("""CREATE TABLE IF NOT EXISTS observations(
            observationID INTEGER NOT NULL PRIMARY KEY,
            observationVal TEXT NOT NULL,
            timestampID INTEGER NOT NULL,
            FOREIGN KEY (timestampID) REFERENCES timestamps(timestampID)
            );""")
        create_table(conn, new_table_timestamps)
        create_table(conn, new_table_observations)

        # insert new rows into tables.
        timestamp = '2020-07-10 10:20:05.123'
        # create new timestamp entry and get id of the new row.
        timestamp_id = insert_timestamp(conn, timestamp)
        observation = 'Test Observation #1.'
        # create new observation entry and link to a timestamp.
        observation_id = insert_observation(conn, observation, timestamp_id)

    else:  # print error if database connection fails.
        print('Error in database connection.')


if __name__ == '__main__':
    main()
