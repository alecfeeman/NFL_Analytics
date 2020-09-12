# Scrape Data from https://www.pro-football-reference.com
# %%
from typing import Any

import pandas as pd
import scrapy
import requests
from bs4 import BeautifulSoup
import csv
from abc import ABC
# %%


class NFLYearScraper:
    # TODO
    base_url = 'https://www.pro-football-reference.com/years/2019/week_1.htm'
    """

    """
    def __init__(self, year):
        self._set_year(year)

    # Setters
    def _set_year(self, year):
        if (int(year) < 2020) & (int(year) >= 2000):
            self.year = year
        else:
            raise ValueError()

    def scrape_year(self):
        #TODO
        pass








class NFLWeekScraper:
    base_url = 'https://www.pro-football-reference.com/years/2019/week_1.htm'
    """

    """
    def __init__(self, year, week):
        self._set_year(year)
        self._set_week(week)
        self._html = None

    # Setters
    def _set_year(self, year):
        if (int(year) < 2020) & (int(year) > 2009):
            self.year = year
        else:
            raise ValueError()

    def _set_week(self, week):
        if week in self.weeks:
            self.week = week
        else:
            raise ValueError()

    def scrape_week(self):
        #TODO
        pass












class NFLGameScraper:
    """
    An object that is used to scrape all of the data for a game from pro-football-reference.com
    """
    base_url = 'https://www.pro-football-reference.com/boxscores/'
    weeks = ['week_1', 'week_2', 'week_3', 'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10',
             'week_11', 'week_12', 'week_13', 'week_14', 'week_15', 'week_16', 'week_17', 'Wildcard', 'Divisional',
             'Conf Champ', 'SuperBowl']
    teams = {
        'CDG': ' Arizona Cardinals',
        'ATL': 'Atlanta Falcons',
        'RAV': 'Baltimore Ravens',
        'BUF': 'Buffalo Bills',
        'CAR': 'Carolina Panthers',
        'CHI': 'Chicago Bears',
        'CIN': 'Cincinnati Bengals',
        'CLE': 'Cleveland Browns',
        'DAL': 'Dallas Cowboys',
        'DEN': 'Denver Broncos',
        'DET': 'Detroit Lions',
        'GNB': 'Green Bay Packers',
        'HTX': 'Houston Texans',
        'CLT': 'Indianapolis Colts',
        'JAX': 'Jacksonville Jaguars',
        'KAN': 'Kansas City Chiefs',
        'SDG': 'Los Angeles Chargers',
        'RAM': 'Los Angeles Rams',
        'MIA': 'Miami Dolphina',
        'MIN': 'Minnesota Vikings',
        'NWE': 'New England Patriots',
        'NOR': 'New Orleans Saints',
        'NYG': 'Mew York Giants',
        'NYJ': 'New York Jets',
        'RAI': 'Las Vegas Raiders',
        'PHI': 'Philadelphia Eagles',
        'PIT': 'Pittsburgh Steelers',
        'SFO': 'San Fransisco 49ers',
        'SEA': 'Seattle Seahawks',
        'TAM': 'Tampa Bay Buccaneers',
        'OTI': 'Tennessee Titans',
        'WAS': 'Washington Football Team'
    }

    def __init__(self, year, week, home, away):
        self._set_year(year)
        self._set_week(week)
        self._set_home(home)
        self._set_away(away)
        self._id = self._generate_id()
        self._html = None
        self._game_info = None
        self._officials = None
        self._team_stats = None
        self._pass_rush_receive = None
        self._defense = None
        self._kick_punt_return = None
        self._kicking_punting = None
        self._advanced_passing = None
        self._advanced_rushing = None
        self._advanced_receiving = None
        self._advanced_defense = None
        self._starters = None
        self._snap_counts = None
        self._drives = None
        self._play_by_play = None
        self.scrape_game()

    # Setters
    def _set_year(self, year):
        if (int(year) < 2020) & (int(year) > 2009):
            self.year = year
        else:
            raise ValueError()

    def _set_week(self, week):
        if week in self.weeks:
            self.week = week
        else:
            raise ValueError()

    def _set_home(self, home):
        if self._check_team(home):
            self.home = home
        else:
            raise ValueError()

    def _set_away(self, away):
        if self._check_team(away):
            self.away = away
        else:
            raise ValueError()

    def _check_team(self, team):
        if team.upper() in self.teams.keys():
            return True
        else:
            return False

    # Methods to download the HTML for the page
    def scrape_game(self):
        self._html = requests.get()
        self._game_info = self._scrape_game_info()
        self._officials = self._scrape_officials()
        self._team_stats = self._scrape_team_stats()
        self._pass_rush_receive = self._scrape_pass_rush_receive()
        self._defense = self._scrape_defense()
        self._kick_punt_return = self._scrape_kick_punt_return()
        self._kicking_punting = self._scrape_kicking_punting()
        self._advanced_passing = self._scrape_advanced_passing()
        self._advanced_rushing = self._scrape_advanced_rushing()
        self._advanced_receiving = self._scrape_advanced_receiving()
        self._advanced_defense = self._scrape_advanced_defense()
        self._starters = self._scrape_starters()
        self._snap_counts = self._scrape_snap_counts()
        self._drives = self._scrape_drives()
        self._play_by_play = self._scrape_play_by_play()

    def html_table_to_pandas(self, outfile_path, html):
        outfile = open(outfile_path, "w", newline='')
        writer = csv.writer(outfile)
        # need to work this part out
        tree = BeautifulSoup(html, "lxml")
        table_tag = tree.select("table")[0]
        tab_data = [[item.text for item in row_data.select("th,td")]
                    for row_data in table_tag.select("tr")]

        for data in tab_data:
            writer.writerow(data)
            print(' '.join(data))

    # Methods to scrape data from html
    def _generate_id(self):
        """
        Generate an ID for a game as year, week, home team, away team.
        Example: 2019week_1CLEDEN
        :return: A unique string ID for a game.
        """
        return str(self.year) + str(self.week) + str(self.home) + str(self.away)

    def _scrape_game_info(self):
        #TODO
        return pd.DataFrame()

    def _scrape_officials(self):
        # TODO
        return pd.DataFrame()

    def _scrape_team_stats(self):
        # TODO
        return 1

    def _scrape_pass_rush_receive(self):
        # TODO
        return 1

    def _scrape_defense(self):
        # TODO
        return 1

    def _scrape_kick_punt_return(self):
        # TODO
        return 1

    def _scrape_kicking_punting(self):
        # TODO
        return 1

    def _scrape_advanced_passing(self):
        # TODO
        return 1

    def _scrape_advanced_rushing(self):
        # TODO
        return 1

    def _scrape_advanced_receiving(self):
        # TODO
        return 1

    def _scrape_advanced_defense(self):
        # TODO
        return 1

    def _scrape_starters(self):
        # TODO
        return 1

    def _scrape_snap_counts(self):
        # TODO
        return 1

    def _scrape_drives(self):
        # TODO
        return 1

    def _scrape_play_by_play(self):
        # TODO
        return 1

    # Getter methods
    def get_id(self):
        return self._id

    def get_game_info(self):
        return self._game_info

    def get_officials(self):
        return self._officials

    def get_team_stats(self):
        return self._team_stats

    def get_pass_rush_receive(self):
        return self._pass_rush_receive

    def get_defense(self):
        return self._defense

    def get_kick_punt_return(self):
        return self._kick_punt_return

    def get_kicking_punting(self):
        return self._kicking_punting

    def get_advanced_passing(self):
        return self._advanced_passing

    def get_advanced_rushing(self):
        return self._advanced_rushing

    def get_advanced_receiving(self):
        return self._advanced_receiving

    def get_advanced_defense(self):
        return self._advanced_defense

    def get_starters(self):
        return self._starters

    def get_snap_counts(self):
        return self._snap_counts

    def get_drives(self):
        return self._drives

    def get_play_by_play(self):
        return self._play_by_play

    def save(self, filetype):
        if filetype == 'csv':
            self.save_csv()
        elif filetype == 'parquet':
            self.save_parquet()

    def save_csv(self):
        self.get_game_info().to_csv(self.get_id() + '_game_info.csv')
        self.get_officials().to_csv(self.get_id() + '_officials.csv')
        self.get_team_stats().to_csv(self.get_id() + '_team_stats.csv')
        self.get_pass_rush_receive().to_csv(self.get_id() + '_pass_rush_receive.csv')
        self.get_defense().to_csv(self.get_id() + '_defense.csv')

    def save_parquet(self):

        pass


base_url = 'https://www.pro-football-reference.com/years/'




def scrape_year(year):
    """
    A function to get all of the games that occured in a given year.

    :param year: The year of the game, a string.
    :return:
    """
    games = dict()
    weeks = ['week_1', 'week_2', 'week_3', 'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10',
             'week_11', 'week_12', 'week_13', 'week_14', 'week_15', 'week_16', 'week_17', 'Wildcard', 'Divisional',
             'Conf Champ', 'SuperBowl']
    for week in weeks:
        scrape_week(year, week)


def scrape_week(year, week):
    """
    A function to get all of the games that occured in a given week.

    :param year: The year of the game, a string.
    :param week: The week of the game, a string.
    :return: A dictionary of games that occured in the week and the respective URL.
    """
    scrape_url = base_url + str(year) + '/' + week + '.htm'
    return


