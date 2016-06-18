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


cur.execute('drop table if exists mls_shots;')
create_table = """
    create table mls_shots (
        game_id int,
        shot_id bigint,
        team varchar(20),
        outcome varchar(20),
        x1 decimal(4, 1),
        y1 decimal(4, 1),
        x2 decimal(4, 1),
        y2 decimal(4, 1));"""

cur.execute(create_table)

data = pd.read_csv('shots_data.csv')
data = data[['game_id', 'shot_id', 'team', 'outcome', 'x1', 'y1', 'x2', 'y2']]
data['x1'] = data['x1'].round(1)
data['y1'] = data['y1'].round(1)
data['x2'] = data['x2'].round(1)
data['y2'] = data['y2'].round(1)
data.to_csv('shots_data.csv', index=False)

path = absolute_path_to('shots_data.csv')


load_data = """
    load data infile '{}' into table mls_shots
      fields terminated by ','
      ignore 1 lines;
""".format(path)

cur.execute(load_data)

db.commit()
cur.close()
