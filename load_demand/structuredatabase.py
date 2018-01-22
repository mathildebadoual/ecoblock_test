import sqlite3

conn = sqlite3.connect('astrodek.sqlite')
cur = conn.cursor()

#Create scripts to drop tables and create tables

drop_table_eb_data_raw = ("DROP TABLE IF EXISTS" +
            "[" + "data_raw" + "]")

drop_table_eb_data_clean = ("DROP TABLE IF EXISTS" +
            "[" + "data_clean" + "]")

drop_table_data_results = ("DROP TABLE IF EXISTS " +
            "[" + "data_results" + "]" )

create_table_eb_data_raw = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "data_raw" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            reading TEXT,
            date DATE,
            day INTEGER,
            timestamp TIMESTAMP,
            season TEXT,
            load_demand FLOAT,
            building TEXT,
            bill TEXT)""")

create_table_eb_data_clean = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "data_clean" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            building TEXT,
            day INTEGER,
            date_time DATETIME,
            season TEXT,
            time TIME,
            readings INTEGER,
            total_demand FLOAT,
            apt_average FLOAT,
            demand_building FLOAT,
            UNIQUE (building, season, day, date_time))""")


create_table_data_results = ("CREATE TABLE IF NOT EXISTS " +
            "[" + "data_results" + "]" +
            """ (id INTEGER PRIMARY KEY UNIQUE,
            profile_number INTEGER,
            date DATE,
            timestamp TIMESTAMP,
            season TEXT,
            load_demand FLOAT,
            scenario TEXT)""")

#Drop and create tables
cur.execute(drop_table_eb_data_raw)
cur.execute(drop_table_eb_data_clean)
cur.execute(drop_table_data_results)
cur.execute(create_table_eb_data_raw)
cur.execute(create_table_eb_data_clean)
cur.execute(create_table_data_results)

conn.commit()
