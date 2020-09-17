#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrape Data from https://www.pro-football-reference.com
"""
__author__ = "Alec Feeman"
__copyright__ = "Copyright 2020, Alec Feeman"
__credits__ = ["Alec Feeman"]
__license__ = "GPL"
__version__ = "v0.1.0-alpha"
__date__ = "09/16/2020"
__maintainer__ = "Alec Feeman"
__email__ = "afeeman@icloud.com"
__status__ = "Development"

# %%
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
import re
import re


# %%
comm = re.compile("<!--|-->")


def html_to_pandas(html):
    """
    A function to convert a html table to a pandas dataframe.

    :param html: A html table.
    :type html: BeautifulSoup tag object
    :return: The converted table.
    :rtype: Pandas Dataframe
    """
    rows = []
    for r in html.find_all('tr'):
        row = []
        for i in r.find_all(['th', 'td']):
            if len(i) > 0:
                row.append(str(i.contents[0]))
            else:
                row.append(None)
        rows.append(row)
    return pd.DataFrame(rows)


#%%
class NFLDraftScraper():
    pass


#%%
class NFLCombineScraper():
    pass


#%%
class NFLYearScraper:
    """

    """
    # TODO
    base_url = 'https://www.pro-football-reference.com/years/2019/week_1.htm'

    def __init__(self, year):
        self._set_year(year)

    # Setters
    def _set_year(self, year):
        if (int(year) < 2020) & (int(year) >= 2000):
            self.year = year
        else:
            raise ValueError()

    def scrape_year(self):
        # TODO
        pass


#%%
class NFLWeekScraper:
    """
    A class to

    Attributes
    ----------

    Methods
    ----------

    """
    base_url = 'https://www.pro-football-reference.com/years/'
    weeks = ['week_1', 'week_2', 'week_3', 'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10',
             'week_11', 'week_12', 'week_13', 'week_14', 'week_15', 'week_16', 'week_17', 'Wildcard', 'Divisional',
             'Conf Champ', 'SuperBowl']

    def __init__(self, year, week):
        self._set_year(year)
        self._set_week(week)
        self._html = None
        self.games = list()

    # Setters
    def _set_year(self, year):
        if (int(year) <= 2020) & (int(year) >= 1970):
            self.year = year
        else:
            raise ValueError()

    def _set_week(self, week):
        if week in self.weeks:
            self.week = week
        else:
            raise ValueError()

    def scrape_week(self):
        self._html = BeautifulSoup(requests.get(self.base_url + str(self.year) + '/' + self.week + '.htm').content,
                                   'html.parser')
        for g in self._html.find_all("div", {"class": "game_summary"}):
            self.games.append(NFLGameScraper(
                year=self.year,
                week=self.week,
                winner=g.find('tr', {'class': 'winner'}).td.a.get_text(),
                loser=g.find('tr', {'class': 'loser'}).td.a.get_text(),
                link=g.find('td', {'class': 'gamelink'}).find('a', href=True)['href']
            ))

    def scrape_games(self):
        for g in self.games:
            g.scrape_game()

    def save_week_data(self):
        for g in self.games:
            g.save('parquet')


#%%
class NFLGameScraper:
    """
    An object that is used to scrape all of the data for a game from pro-football-reference.com
    """
    base_url = 'https://www.pro-football-reference.com/'
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

    def __init__(self, year, week, winner, loser, link):
        self._set_year(year)
        self._set_week(week)
        self._set_winner(winner)
        self._set_loser(loser)
        # TODO create set link method that removes any starting slash
        self.link = link
        self._id = self._generate_id()
        self._html = None
        self._scoring = None
        self._linescore = None
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

    def _set_winner(self, winner):
        if self._check_team(winner):
            self.winner = winner
        else:
            raise ValueError()

    def _set_loser(self, loser):
        if self._check_team(loser):
            self.loser = loser
        else:
            raise ValueError()

    def _check_team(self, team):
        if team.upper() in self.teams.keys():
            return True
        else:
            return False

    # Methods to download the HTML for the page
    def scrape_game(self):
        # TODO
        self._html = BeautifulSoup(comm.sub('', requests.get(self.base_url + self.link).text), 'lxml')
        self._scrape_game_info()
        self._scrape_officials()
        self._scrape_team_stats()
        self._scrape_pass_rush_receive()
        self._scrape_defense()
        self._scrape_kick_punt_return()
        self._scrape_kicking_punting()
        self._scrape_advanced_passing()
        self._scrape_advanced_rushing()
        self._scrape_advanced_receiving()
        self._scrape_advanced_defense()
        self._scrape_starters()
        self._scrape_snap_counts()
        self._scrape_drives()
        self._scrape_play_by_play()

    # Methods to scrape data from html
    def _generate_id(self):
        """
        Generate an ID for a game as year, week, home team, away team.
        Example: 2019week_1CLEDEN
        :return: A unique string ID for a game.
        """
        return str(self.year) + str(self.week) + str(self.home) + str(self.away)

    def _scrape_scoring(self):
        scoring_html = self._html.find('table', {'id': 'scoring'})
        scoring = html_to_pandas(scoring_html)
        scoring.columns = scoring.iloc[0]
        scoring.drop(scoring.index[0], inplace=True)
        self._scoring = scoring

    def _scrape_linescore(self):
        linescore_html = self._html.find('table', {'class': 'linescore'})
        linescore = html_to_pandas(linescore_html)
        linescore.drop(columns=0, inplace=True)
        linescore.columns = ['Team', 'Q1', 'Q2', 'Q3', 'Q4', 'FINAL']
        linescore = linescore.loc[1:]
        self._linescore = linescore

    def _scrape_game_info(self):
        # TODO, make sure to also get coaches, stadium
        game_info_html = self._html.find('table', {'id': 'game_info'})
        game_info = html_to_pandas(game_info_html)

        self._game_info(game_info)

    def _scrape_officials(self):
        officials_html = self._html.find('table', {'id': 'officials'})
        officials = html_to_pandas(officials_html)
        officials.columns = ['position', 'official']
        officials.set_index('position', inplace=True)
        officials.drop('Officials', inplace=True)
        self._officials(officials)

    def _scrape_team_stats(self):
        team_stats_html = self._html.find('table', {'id': 'team_stats'})
        team_stats = html_to_pandas(team_stats_html)
        team_stats.columns = ['stat', 'visitor', 'rows']
        team_stats.loc[0, 'stat'] = 'Teams'
        team_stats.set_index('stat', inplace=True)
        self._team_stats(team_stats)

    def _scrape_pass_rush_receive(self):
        # TODO
        pass_rush_receive = pd.DataFrame()

        self._pass_rush_receive(pass_rush_receive)

    def _scrape_defense(self):
        # TODO
        defense = pd.DataFrame()

        self._defense(defense)

    def _scrape_kick_punt_return(self):
        # TODO
        kick_punt_return = pd.DataFrame()

        self._kick_punt_return(kick_punt_return)

    def _scrape_kicking_punting(self):
        # TODO
        kicking_punting = pd.DataFrame()

        self._kicking_punting(kicking_punting)

    def _scrape_advanced_passing(self):
        # TODO
        advanced_passing = pd.DataFrame()

        self._advanced_passing(advanced_passing)

    def _scrape_advanced_rushing(self):
        # TODO
        advanced_rushing = pd.DataFrame()

        self._advanced_rushing(advanced_rushing)

    def _scrape_advanced_receiving(self):
        # TODO
        advanced_receiving = pd.DataFrame()

        self._advanced_receiving(advanced_receiving)

    def _scrape_advanced_defense(self):
        # TODO
        advanced_defense = pd.DataFrame()

        self._advanced_defense(advanced_defense)

    def _scrape_starters(self):
        # TODO
        starters = pd.DataFrame()

        self._starters(starters)

    def _scrape_snap_counts(self):
        # TODO
        snap_counts = pd.DataFrame()

        self._snap_counts(snap_counts)

    def _scrape_drives(self):
        # TODO
        drives = pd.DataFrame()

        self._drives(drives)

    def _scrape_play_by_play(self):
        # TODO
        play_by_play = pd.DataFrame()

        self._play_by_play(play_by_play)

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

    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        self.get_game_info().to_csv(filepath + self.get_id() + '_game_info.csv')
        self.get_officials().to_csv(filepath + self.get_id() + '_officials.csv')
        self.get_team_stats().to_csv(filepath + self.get_id() + '_team_stats.csv')
        self.get_pass_rush_receive().to_csv(filepath + self.get_id() + '_pass_rush_receive.csv')
        self.get_defense().to_csv(filepath + self.get_id() + '_defense.csv')
        self.get_kick_punt_return().to_csv(filepath + self.get_id() + '_kick_punt_return.csv')
        self.get_kicking_punting().to_csv(filepath + self.get_id() + '_kicking_punting.csv')
        self.get_advanced_passing().to_csv(filepath + self.get_id() + '_advanced_passing.csv')
        self.get_advanced_rushing().to_csv(filepath + self.get_id() + '_advanced_rushing.csv')
        self.get_advanced_receiving().to_csv(filepath + self.get_id() + '_advanced_receiving.csv')
        self.get_advanced_defense().to_csv(filepath + self.get_id() + '_advanced_defense.csv')
        self.get_starters().to_csv(filepath + self.get_id() + '_starters.csv')
        self.get_snap_counts().to_csv(filepath + self.get_id() + '_snap_counts.csv')
        self.get_drives().to_csv(filepath + self.get_id() + '_drives.csv')
        self.get_play_by_play().to_csv(filepath + self.get_id() + '_play_by_play.csv')

    def save_parquet(self, filepath):
        self.get_game_info().to_parquet(filepath + self.get_id() + '_game_info.csv')
        self.get_officials().to_parquet(filepath + self.get_id() + '_officials.csv')
        self.get_team_stats().to_parquet(filepath + self.get_id() + '_team_stats.csv')
        self.get_pass_rush_receive().to_parquet(filepath + self.get_id() + '_pass_rush_receive.csv')
        self.get_defense().to_parquet(filepath + self.get_id() + '_defense.csv')
        self.get_kick_punt_return().to_parquet(filepath + self.get_id() + '_kick_punt_return.csv')
        self.get_kicking_punting().to_parquet(filepath + self.get_id() + '_kicking_punting.csv')
        self.get_advanced_passing().to_parquet(filepath + self.get_id() + '_advanced_passing.csv')
        self.get_advanced_rushing().to_parquet(filepath + self.get_id() + '_advanced_rushing.csv')
        self.get_advanced_receiving().to_parquet(filepath + self.get_id() + '_advanced_receiving.csv')
        self.get_advanced_defense().to_parquet(filepath + self.get_id() + '_advanced_defense.csv')
        self.get_starters().to_parquet(filepath + self.get_id() + '_starters.csv')
        self.get_snap_counts().to_parquet(filepath + self.get_id() + '_snap_counts.csv')
        self.get_drives().to_parquet(filepath + self.get_id() + '_drives.csv')
        self.get_play_by_play().to_parquet(filepath + self.get_id() + '_play_by_play.csv')
