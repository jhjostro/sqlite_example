# SQLite Example #

A simple example of working with an SQLite database in python.

Install SQLite3 on your system to get started.

The connect_to_database function allows you to either create or connect to an existing sqlite database file by specifying a path.

You can see how to create new tables using the create_table function. This example creates two new tables, timestamps and observations. observations has a foreign key constraint on timestampID.

The example contains two functions, insert_timestamp and insert_observation, that show how you can easily insert new rows into specific database tables.

Finally, an example query is included, query_observations_by_date, showing to query the observations table by a given date.
