import MySQLdb
import pandas as pd
import os

db = MySQLdb.connect(host="localhost", user="ford", db="ss",
                     passwd="soccerstatistic")
cur = db.cursor()

def absolute_path_to(file_name):
    for root, _, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
        if file_name in files:
            return os.path.join(root, file_name)


cur.execute('drop table if exists epl_club_seasons;')
create_table = """
    create table epl_club_seasons (
        club varchar(100),
        year char(9),
        gp int,
        wins int,
        draws int,
        losses int,
        gf int,
        ga int,
        pk_goals int,
        shots int,
        crosses int,
        offsides int,
        saves int,
        own_goals int,
        shutouts int,
        blocks int,
        clearances int,
        fouls int,
        cards int);"""

cur.execute(create_table)

data = pd.read_csv('club_data.csv')
data = data[['name', 'year', 'gp', 'wins', 'draws', 'losses', 'gf', 'ga',
             'pk_goals', 'shots', 'crosses', 'offsides', 'saves', 'own_goals',
             'shutouts', 'blocks', 'clearances', 'fouls', 'cards']]
data.to_csv('club_data.csv', index=False)

path = absolute_path_to('club_data.csv')


load_data = """
    load data infile '{}' into table epl_club_seasons
      fields terminated by ','
      ignore 1 lines;
""".format(path)

cur.execute(load_data)

db.commit()
cur.close()
