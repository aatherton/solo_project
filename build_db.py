# -*- coding: utf-8 -*-

"""### import dependancies ###"""

import mysql.connector, csv

"""### define functions ###"""

def ez_exe(db, do):
    """takes a db connection, executes do, and updates the db"""
    cursor = db.cursor()
    cursor.execute(do)
    cursor.close()
    db.commit()
        

"""### declare constants ###"""

DATABASE = mysql.connector.connect(
        host = "localhost",
        user = "root",
        db = "rplace"
        )

DATA_LOCATION = "tile_placements.csv"
# location of the main dataset
COLORSWAP = {
    0: "#FFFFFF",
    1: "#E4E4E4",
    2: "#888888",
    3: "#222222",
    4: "#FFA7D1",
    5: "#E50000",
    6: "#E59500",
    7: "#A06A42",
    8: "#E5D900",
    9: "#94E044",
    10: "#02BE01",
    11: "#00E5F0",
    12: "#0083C7",
    13: "#0000EA",
    14: "#E04AFF",
    15: "#820080"
}

"""### beyblade! let 'er rip! ###"""

# drop the tables we are using
for each in ["actions", "colorswap"]:
    ez_exe(DATABASE, f"drop table if exists {each};")
# create the colorswap table
ez_exe(DATABASE, """
       create table colorswap(
       color tinyint(2) primary key,
       hex varchar(14)
       );
       """)

# populate the colorswap table
for each in range(16):
    ez_exe(DATABASE, f"""
           insert into colorswap
           values ({each}, "{COLORSWAP[each]}");
           """)
# create the actions table
ez_exe(DATABASE, """
       create table actions(
       id int(125) not null auto_increment primary key,
       ts bigint(15),
       user varchar(255),
       x_coordinate int(5),
       y_coordinate int(5),
       color tinyint(2)
       );
       """)
# populate the actions table
counter = 1
with open(DATA_LOCATION) as x:
    reader = csv.reader(x)
    next(reader)
    for each in reader:
        print(f"writing record #{counter}")
        ez_exe(DATABASE, f"""
               insert into actions
               (ts, user, x_coordinate, y_coordinate, color)
               values ({str(each)[1:-1]});
               """)
        counter = counter + 1