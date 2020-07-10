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

    return cur.lastrowid


def get_observations_by_date(conn: sqlite3.Connection, date: str) -> list:
    """
    Function to query the observations table by a given date.
    
    First querys the timestamp table to find all timestampID's related to the
    given date, then querys the observations table based on those timestampID
    values. Returns a list of observations.
    """

    # query timestamps table using date to get matching timestampID's.
    timestamps_query = str('SELECT timestampID FROM timestamps WHERE'
                           + ' DATE(timestampVal) = "' + date + '"')
    try:
        cur = conn.cursor()
        cur.execute(timestamps_query)
        results = cur.fetchall()
        # extract the timestamp id's into a useable list for next query.
        timestamp_list = [str(row[0]) for row in results]
        sep = ','
        timestamp_ids = sep.join(timestamp_list)
    except Error as err:
        print(err)

    # query observations using selected timestampID's.
    observations_query = str('SELECT observationVal FROM observations WHERE '
                             + 'timestampID IN (' + str(timestamp_ids) + ')')
    try:
        cur = conn.cursor()
        cur.execute(observations_query)
        query_results = cur.fetchall()
    except Error as err:
        print(err)

    return query_results


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
        timestamp = '2020-07-10 10:20:05.123'  # example timestamp value.
        timestamp_id = insert_timestamp(conn, timestamp)
        observation = 'Test Observation #1.'  # example observation value.
        insert_observation(conn, observation, timestamp_id)

        # query the table
        date = '2020-07-10'  # example date to query the observations table.
        results = get_observations_by_date(conn, date)
        print(results)

    else:  # print error if database connection fails.
        print('Error in database connection.')


if __name__ == '__main__':
    main()
