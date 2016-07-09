import luigi
from luigi import LocalTarget
import yaml
import os
import sys
import time
import MySQLdb
from mls.mls_scrape import create_club_seasons, club_seasons
from mls.mls_scrape import create_player_seasons, player_seasons



# Helper Function
def absolute_path_to(file_name):
    for root, _, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
        if file_name in files:
            return os.path.join(root, file_name)

# mysql config
with open(absolute_path_to('config.yaml'), 'r') as f:
    doc = yaml.load(f)
    database = doc['sql']['database']
    host = doc['sql']['host']
    user = doc['sql']['user']
    password = doc['sql']['password']

db = MySQLdb.connect(host=host, user=user, db=database, passwd=password)
cur = db.cursor()


class Create_MLS_club(luigi.Task):

    def requires(self):
        return []

    def output(self):
        return LocalTarget('mls/markers/mls_club_init.txt')

    def run(self):
        create_club_seasons(cur)
        with self.output().open('w') as f:
            f.write('MLS club table created!')


class Create_MLS_player(luigi.Task):

    def requires(self):
        return []

    def output(self):
        return LocalTarget('mls/markers/mls_player_init.txt')

    def run(self):
        create_player_seasons(cur)
        with self.output().open('w') as f:
            f.write('MLS player table created!')


class MLS_club(luigi.Task):
    year = luigi.Parameter(default='2016') # year of season to scrape
    season = luigi.Parameter(default='REG') # REG: regular, PS: postseason
    batch = luigi.Parameter(default=time.strftime("%Y%m%d"))

    def requires(self):
        return [Create_MLS_club()]

    def output(self):
        return LocalTarget('mls/markers/mls_club_{}_{}_{}'.format(self.year, self.season, self.batch))

    def run(self):
        club_seasons(self.year, self.season, self.batch, cur)
        db.commit()
        with self.output().open('w') as f:
            f.write('MLS {} season scraped for year {}'.format(self.season, self.year))


class MLS_player(luigi.Task):
    year = luigi.Parameter(default='2016') # year of season to scrape
    season = luigi.Parameter(default='REG') # REG: regular, PS: postseason
    batch = luigi.Parameter(default=time.strftime("%Y%m%d"))

    def requires(self):
        return [Create_MLS_player()]

    def output(self):
        return LocalTarget('mls/markers/mls_player_{}_{}_{}'.format(self.year, self.season, self.batch))

    def run(self):
        player_seasons(self.year, self.season, self.batch, cur)
        db.commit()
        with self.output().open('w') as f:
            f.write('MLS {} player scraped for year {} and batch id {}'.format(self.season, self.year, self.batch))


class MLS(luigi.Task):
    year = luigi.ListParameter(default=['2016']) # years of seasons to scrape
    season = luigi.ListParameter(default=['REG']) # REG: regular, PS: postseason
    batch = luigi.Parameter(default=time.strftime("%Y%m%d"))

    def requires(self):
        for y in self.year:
            for s in self.season:
                yield [MLS_player(y, s, self.batch), MLS_club(y, s, self.batch)]

    def output(self):
        return LocalTarget('mls/markers/mls_batch_{}'.format(self.batch))

    def run(self):
        with self.output().open('w') as f:
            f.write('MLS batch {} done!'.format(self.batch))


class MLS_daily(luigi.Task):
    year = luigi.ListParameter(default=['2016']) # years of seasons to scrape
    season = luigi.ListParameter(default=['REG']) # REG: regular, PS: postseason
    batch = time.strftime("%Y%m%d")

    def requires(self):
        return [MLS(self.year, self.season, self.batch)]

    def output(self):
        pass

    def run(self):
        fd = open(absolute_path_to('remove_duplicates.sql'), 'r')
        query = fd.read()
        cur.execute(query)



if __name__ == '__main__':
    luigi.run()
