import pandas as pd

year = 2016

d = pd.read_csv('shot_data_{y}.csv'.format(y=year))
d = d[pd.notnull(d['team'])]
d.drop_duplicates(inplace=True)
d['game_id'] = d['game_id'].astype(int)
d['shot_id'] = d['shot_id'].astype(int)

d = d[['game_id', 'team', 'shot_id', 'outcome', 'x1', 'y1', 'x2', 'y2']]

d.to_csv('shot_data_{y}.csv'.format(y=year), index=False)
