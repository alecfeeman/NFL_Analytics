#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: Make sure all private member variables have a getter and it is used
# TODO: Think about how to leverage abstraction and inheritance
# TODO: Document Classes and Functions
"""
Scrape Data from https://www.pro-football-reference.com


-----------------------------------------------------------------------------
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "Alec Feeman"
__copyright__ = "Copyright 2020, Alec Feeman"
__credits__ = ["Alec Feeman"]
__license__ = "GPLv3"
__version__ = "v0.1.0-alpha"
__date__ = "09/16/2020"
__maintainer__ = "Alec Feeman"
__email__ = "afeeman@icloud.com"
__status__ = "Development"

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
import bs4
import re
import logging
import time
import os
import random
from project_tools import bidict, ScraperProxy

# %%
comm = re.compile("<!--|-->")
MIN_YEAR = 1970
WEEKS = ['week_1', 'week_2', 'week_3', 'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10',
         'week_11', 'week_12', 'week_13', 'week_14', 'week_15', 'week_16', 'week_17', 'week_18', 'week_19',
         'week_20', 'week_21']
TEAMS = bidict({
    'CDG': ['Arizona Cardinals', 'Phoenix Cardinals', 'St. Louis Cardinals'],
    'ATL': ['Atlanta Falcons'],
    'RAV': ['Baltimore Ravens'],
    'BUF': ['Buffalo Bills'],
    'CAR': ['Carolina Panthers'],
    'CHI': ['Chicago Bears'],
    'CIN': ['Cincinnati Bengals'],
    'CLE': ['Cleveland Browns'],
    'DAL': ['Dallas Cowboys'],
    'DEN': ['Denver Broncos'],
    'DET': ['Detroit Lions'],
    'GNB': ['Green Bay Packers'],
    'HTX': ['Houston Texans'],
    'CLT': ['Indianapolis Colts', 'Baltimore Colts'],
    'JAX': ['Jacksonville Jaguars'],
    'KAN': ['Kansas City Chiefs'],
    'SDG': ['Los Angeles Chargers', 'San Diego Chargers'],
    'RAM': ['Los Angeles Rams', 'St. Louis Rams'],
    'MIA': ['Miami Dolphins'],
    'MIN': ['Minnesota Vikings'],
    'NWE': ['New England Patriots', 'Boston Patriots'],
    'NOR': ['New Orleans Saints'],
    'NYG': ['Mew York Giants'],
    'NYJ': ['New York Jets'],
    'RAI': ['Las Vegas Raiders', 'Los Angeles Raiders', 'Oakland Raiders'],
    'PHI': ['Philadelphia Eagles'],
    'PIT': ['Pittsburgh Steelers'],
    'SFO': ['San Fransisco 49ers'],
    'SEA': ['Seattle Seahawks'],
    'TAM': ['Tampa Bay Buccaneers'],
    'OTI': ['Tennessee Titans', 'Houston Oilers', 'Tennessee Oilers'],
    'WAS': ['Washington Football Team', 'Washington Redskins']
})


# %%

def check_team(team):
    """
    Check if a team abbreviation is valid. If a valid full team name is passed convert it to the abbreviation.

    Args:

    Returns:

    Raises:
        TypeError: The team arg must be a string.
    """
    if team.upper() in TEAMS.keys():
        return team.upper()
    elif team in TEAMS.values():
        return TEAMS.inverse[team]
    else:
        return False


def html_to_pandas(html):
    """
    A function to convert a html table to a pandas dataframe.

    Args:
        html: BeautifulSoup tag object of a html table.
    Returns:
        A Pandas Dataframe of the converted table.
    Raises:
        TypeError: The html arg must be passed as a BeautifulSoup Tag object
    """
    if not isinstance(html, bs4.Tag):
        raise TypeError('The html arg must be passed as a BeautifulSoup Tag object')

    rows = []
    for r in html.find_all('tr'):
        row = []
        for i in r.find_all(['th', 'td']):
            if len(i) > 0:
                row.append(' '.join([str(c) for c in i.contents]))
            else:
                row.append(None)
        rows.append(row)
    return pd.DataFrame(rows)


def clean_stat_table(df, kind):
    """

    """
    if kind == 'regular':
        df.columns = df.iloc[1]
    elif kind == 'advanced':
        df.columns = df.iloc[0]
    else:
        raise  # TODO: better error handling
    indexes_to_drop = df.loc[df['Player'] == 'Player'].index.values.tolist() + \
                      df.loc[df['Player'].isnull()].index.values.tolist()
    df.drop(index=indexes_to_drop, inplace=True)
    return df


def check_year(year):
    if (int(year) < int(time.strftime('%Y'))) & (int(year) >= MIN_YEAR):
        return True
    else:
        return False


# %%
class NFLDraftScraper:
    """
    desc

    Attributes:

    Methods:

    """
    base_url = 'https://www.pro-football-reference.com/years/'

    def __init__(self, year, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_year(year)
        self._html = None
        self._draft_data = None
        self._supplemental_draft_data = None
        self._draft_pick_trades = None
        self._scraper_proxy = scraper_proxy

    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()

    def scrape_draft(self):
        self._logger.info(f"")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + str(self.year) + '/draft.htm'
                                                                        ).text), 'lxml')
        self._scrape_draft_data()
        self._scrape_supplemental_draft_data()
        self._scrape_draft_pick_trades()

    def _scrape_draft_data(self):
        draft_html = self._html.find('table', {'id': 'drafts'})
        draft = html_to_pandas(draft_html)
        cols = []
        draft.columns = cols

    def _scrape_supplemental_draft_data(self):
        pass

    def _scrape_draft_pick_trades(self):
        pass

    def get_draft_data(self):
        return self._draft_data

    def get_supplemental_draft_data(self):
        return self._supplemental_draft_data

    def get_draft_pick_trades(self):
        return self._draft_pick_trades

    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv'),
                 self.get_supplemental_draft_data().to_csv(filepath + self.year + '_supplemental_draft_data.csv'),
                 self.get_draft_pick_trades().to_csv(filepath + self.year + '_draft_pick_trades_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet'),
                 self.get_supplemental_draft_data().to_parquet(filepath + self.year + '_supplemental_draft_data.csv'),
                 self.get_draft_pick_trades().to_parquet(filepath + self.year + '_draft_pick_trades_data.csv')
                 ]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLCombineScraper:
    # TODO
    """
    desc

    Attributes:

    Methods:

    """
    base_url = 'https://www.pro-football-reference.com/draft/2020-combine.htm'

    def __init__(self, year, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_year(year)
        self._scraper_proxy = scraper_proxy
        self._html = None

    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()

    def scrape_combine(self):
        self._logger.info(f"")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + '').text), 'lxml')


    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLInjuryScraper:
    # TODO
    """
    desc

    Attributes:

    Methods:

    """
    base_url = 'https://www.pro-football-reference.com/teams/'

    def __init__(self, year, team, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_team(team)
        self._set_year(year)
        self._scraper_proxy = scraper_proxy
        self._html = None

    def _set_team(self, team):
        team = check_team(team)
        if team:
            self.team = team
        else:
            raise ValueError('An invalid team abbreviation or name was passed')

    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()

    def scrape_injuries(self):
        self._logger.info(f"Scraping injury data for: {str(self.team)} in {str(self.year)}")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + str(self.team).lower() + '/' +
                                                                        str(self.year) + '_injuries.htm').text), 'lxml')


    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLCoachScraper:
    # TODO
    """
        desc

        Attributes:

        Methods:

    """
    base_url = 'https://www.pro-football-reference.com/coaches/ShulDo0.htm'

    def __init__(self, coach, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_coach(coach)
        self._scraper_proxy = scraper_proxy
        self._html = None

    def _set_coach(self, coach):
        self.coach = coach

    def scrape_coach(self):
        self._logger.info(f"")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + '').text), 'lxml')


    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLPlayerScraper:
    # TODO
    """
        desc

        Attributes:

        Methods:

    """
    base_url = 'https://www.pro-football-reference.com/players/A/AndeKe00.htm'

    def __init__(self, player, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_player(player)
        self._scraper_proxy = scraper_proxy
        self._html = None

    def _set_player(self, player):
        self.player = player

    def scrape_player(self):
        self._logger.info(f"")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + '').text), 'lxml')


    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLTravelScraper:
    # TODO
    """
        desc

        Attributes:

        Methods:

    """
    base_url = 'https://www.pro-football-reference.com/teams/cle/2020_travel.htm'

    def __init__(self, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._scraper_proxy = scraper_proxy
        self._html = None


    def save(self, filetype, filepath):
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        if filetype == 'csv':
            self.save_csv(filepath)
        elif filetype == 'parquet':
            self.save_parquet(filepath)

    def save_csv(self, filepath):
        saves = [self.get_draft_data().to_csv(filepath + self.year + '_draft_data.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as csv files")

    def save_parquet(self, filepath):
        saves = [self.get_draft_data().to_parquet(filepath + self.year + '_draft_data.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self.year} as parquet files")


# %%
class NFLGameScraper:
    """
    A class that is used to scrape all of the data for a game from pro-football-reference.com

    Attributes:

    Methods:

    """
    base_url = 'https://www.pro-football-reference.com/'

    def __init__(self, year, week, link, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_year(year)
        self._set_week(week)
        self._set_link(link)
        self._set_id()
        self._scraper_proxy = scraper_proxy
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
        self._logger.info(f"Created game object for game: {self._id}")

    # Setters
    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()

    def _set_week(self, week):
        if week in WEEKS:
            self.week = week
        else:
            raise ValueError()

    def _set_link(self, link):
        """ Remove any starting slash"""
        if not isinstance(link, str):
            raise TypeError()
        if link.startswith('/'):
            self.link = link[1:]

    # Methods to download the HTML for the page
    def scrape_game(self):
        """Get the html for the game page then scrape all of the data out of the html."""
        self._logger.info(f"Requesting html for the game: {self._id}, at the link: {self.link}")
        try:
            self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + self.link).text), 'lxml')
            self._scrape_scoring()
            self._scrape_linescore()
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
        except Exception as e:
            self._logger.error(e)

    # Methods to scrape data from html
    def _set_id(self):
        """
        Generate a unique ID for a game
        Example: 201809090cle
        """
        self._id = self.link[-16:-4]

    def _scrape_scoring(self):
        """Scrape the scoring table for the game and save it as a pandas dataframe"""
        try:
            scoring_html = self._html.find('table', {'id': 'scoring'})
            scoring = html_to_pandas(scoring_html)
            scoring.columns = scoring.iloc[0]
            scoring.drop(scoring.index[0], inplace=True)
            self._scoring = scoring
            self._logger.info(f'Scoring data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Scoring data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_linescore(self):
        """Scrape the linescore table for the game and save it as a pandas dataframe"""
        try:
            linescore_html = self._html.find('table', {'class': 'linescore'})
            linescore = html_to_pandas(linescore_html)
            linescore.columns = linescore.iloc[0]
            linescore.drop(index=0, inplace=True)
            linescore = linescore.loc[1:]
            self._linescore = linescore
            self._logger.info(f'Linescore data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Linescore data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_game_info(self):
        """Scrape the game info as well as the coaches and stadium and save it as a pandas dataframe"""
        try:
            game_info_html = self._html.find('table', {'id': 'game_info'})
            game_info = html_to_pandas(game_info_html)
            # Find the coaches and add them to game info
            coaches = [c.a for c in
                       self._html.find('div', {'class': 'scorebox'}).find_all('div', {'class': 'datapoint'})]
            game_info = game_info.append({0: 'home coach', 1: str(coaches[0])}, ignore_index=True)
            game_info = game_info.append({0: 'away coach', 1: str(coaches[1])}, ignore_index=True)
            # Find the game date and add it to game info
            game_date = self._html.find('div', {'class': 'scorebox_meta'}).find('div').text
            game_info = game_info.append({0: 'date', 1: str(game_date)}, ignore_index=True)
            # Find the game date and add it to game info
            game_time = self._html.find('div', {'class': 'scorebox_meta'}).find_all('div')[1].text
            game_info = game_info.append({0: 'time', 1: str(game_time)}, ignore_index=True)
            # Find the stadium and add it to game info
            stadium = self._html.find('div', {'class': 'scorebox'}).find_all('a')[10]
            game_info = game_info.append({0: 'stadium', 1: str(stadium)}, ignore_index=True)
            # find the home team and add it to game info
            home_team = self._html.find('div', {'class': 'scorebox'}).find_all('a')[2]
            game_info = game_info.append({0: 'home team', 1: str(home_team)}, ignore_index=True)
            # find the away team and add it to game info
            away_team = self._html.find('div', {'class': 'scorebox'}).find_all('a')[7]
            game_info = game_info.append({0: 'away team', 1: str(away_team)}, ignore_index=True)
            self._game_info = game_info
            self._logger.info(f'Game info data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Game info data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_officials(self):
        """Scrape the officials for the game and save it as a pandas dataframe"""
        try:
            officials_html = self._html.find('table', {'id': 'officials'})
            officials = html_to_pandas(officials_html)
            officials.columns = ['position', 'official']
            officials.set_index('position', inplace=True)
            officials.drop('Officials', inplace=True)
            self._officials = officials
            self._logger.info(f'Officials data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Officials data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_team_stats(self):
        """Scrape the team stats for the game and save it as a pandas dataframe"""
        try:
            team_stats_html = self._html.find('table', {'id': 'team_stats'})
            team_stats = html_to_pandas(team_stats_html)
            team_stats.columns = ['stat', 'visitor', 'rows']
            team_stats.loc[0, 'stat'] = 'Teams'
            team_stats.set_index('stat', inplace=True)
            self._team_stats = team_stats
            self._logger.info(f'Team stats data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Team stats data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_pass_rush_receive(self):
        """Scrape the offensive player stats for the game and save it as a pandas dataframe"""
        try:
            pass_rush_receive_html = self._html.find('table', {'id': 'player_offense'})
            pass_rush_receive = clean_stat_table(html_to_pandas(pass_rush_receive_html), 'regular')
            cols = ['player', 'team', 'pass_completions', 'pass_attempts', 'passing_yds', 'pass_td',
                    'int_thrown', 'times_sacked', 'yds_lst_sacks', 'long_pass', 'qb_rating', 'rush_attempts',
                    'rush_yards', 'rush_td', 'long_rush', 'pass_targets', 'pass_receptions', 'receive_yards',
                    'receive_td', 'long_reception', 'fumbles', 'fumbles_lst']
            pass_rush_receive.columns = cols
            self._pass_rush_receive = pass_rush_receive
            self._logger.info(f'Offensive player stats data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Offensive player data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_defense(self):
        """Scrape the defensive player stats for the game and save it as a pandas dataframe"""
        try:
            defense_html = self._html.find('table', {'id': 'player_defense'})
            defense = clean_stat_table(html_to_pandas(defense_html), 'regular')
            cols = ['player', 'team', 'ints', 'int_rtn_yards', 'int_rtn_td', 'long_int_rtn', 'passes_defended', 'sacks',
                    'comb_tackles', 'solo_tackles', 'assist_tackles', 'tackles_for_loss', 'qb_hits', 'fumb_rec',
                    'fumb_rtn_yds', 'fumb_rtn_td', 'forced_fumb']
            defense.columns = cols
            self._defense = defense
            self._logger.info(f'Defensive player stats data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Defensive player stats  data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_kick_punt_return(self):
        """Scrape the returns player stats for the game and save it as a pandas dataframe"""
        try:
            kick_punt_return_html = self._html.find('table', {'id': 'returns'})
            kick_punt_return = clean_stat_table(html_to_pandas(kick_punt_return_html), 'regular')
            cols = ['player', 'team', 'kick_rtns', 'kick_rtn_yds', 'kick_yds_per_rtn', 'kick_rtn_td', 'long_kick_rtn',
                    'pnt_rtns', 'pnt_rtn_yds', 'pnt_yds_per_rtn', 'pnt_rtn_td', 'long_pnt_rtn']
            kick_punt_return.columns = cols
            self._kick_punt_return = kick_punt_return
            self._logger.info(f'Kick and punt return data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Kick and punt return data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_kicking_punting(self):
        """Scrape the kicking player stats for the game and save it as a pandas dataframe"""
        try:
            kicking_punting_html = self._html.find('table', {'id': 'kicking'})
            kicking_punting = clean_stat_table(html_to_pandas(kicking_punting_html), 'regular')
            cols = ['player', 'team', 'xp_made', 'xp_attempt', 'fg_made', 'fg_attempted', 'num_pnt', 'pnt_yds',
                    'yds_per_punt', 'lng_pnt']
            kicking_punting.columns = cols
            self._kicking_punting = kicking_punting
            self._logger.info(f'Kicking and punting data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Kicking and punting data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_advanced_passing(self):
        """Scrape the advanced passing player stats for the game and save it as a pandas dataframe"""
        try:
            advanced_passing_html = self._html.find('table', {'id': 'passing_advanced'})
            advanced_passing = clean_stat_table(html_to_pandas(advanced_passing_html), 'advanced')
            self._advanced_passing = advanced_passing
            self._logger.info(f'Advanced passing data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Advanced passing data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_advanced_rushing(self):
        """Scrape the advanced rushing player stats for the game and save it as a pandas dataframe"""
        try:
            advanced_rushing_html = self._html.find('table', {'id': 'rushing_advanced'})
            advanced_rushing = clean_stat_table(html_to_pandas(advanced_rushing_html), 'advanced')
            self._advanced_rushing = advanced_rushing
            self._logger.info(f'Advanced rushing data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Advanced rushing data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_advanced_receiving(self):
        """Scrape the advanced receiving player stats for the game and save it as a pandas dataframe"""
        try:
            advanced_receiving_html = self._html.find('table', {'id': 'receiving_advanced'})
            advanced_receiving = clean_stat_table(html_to_pandas(advanced_receiving_html), 'advanced')
            self._advanced_receiving = advanced_receiving
            self._logger.info(f'Advanced receiving data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Advanced receiving data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_advanced_defense(self):
        """Scrape the advanced receiving player stats for the game and save it as a pandas dataframe"""
        try:
            advanced_defense_html = self._html.find('table', {'id': 'defense_advanced'})
            advanced_defense = clean_stat_table(html_to_pandas(advanced_defense_html), 'advanced')
            self._advanced_defense = advanced_defense
            self._logger.info(f'Advanced defense data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Advanced defense data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_starters(self):
        """Scrape the starters data for the game and save it as a pandas dataframe"""
        try:
            home_starters_html = self._html.find('table', {'id': 'home_starters'})
            home_starters = html_to_pandas(home_starters_html)
            home_starters.columns = home_starters.iloc[0]
            home_starters.drop(index=0, inplace=True)
            home_starters['team'] = 'home'
            away_starters_html = self._html.find('table', {'id': 'vis_starters'})
            away_starters = html_to_pandas(away_starters_html)
            away_starters.columns = away_starters.iloc[0]
            away_starters.drop(index=0, inplace=True)
            away_starters['team'] = 'away'
            self._starters = pd.concat([home_starters, away_starters])
            self._logger.info(f'Team starters data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Team starters data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_snap_counts(self):
        """Scrape the player snap counts data for the game and save it as a pandas dataframe"""
        try:
            cols = ['player', 'pos', 'off_snaps', 'off_pct', 'def_snaps', 'def_pct', 'st_snaps', 'st_pct']
            home_snap_counts_html = self._html.find('table', {'id': 'home_snap_counts'})
            home_snap_counts = html_to_pandas(home_snap_counts_html)
            home_snap_counts.columns = cols
            home_snap_counts.drop(index=[0, 1], inplace=True)
            home_snap_counts['team'] = 'home'
            away_snap_counts_html = self._html.find('table', {'id': 'vis_snap_counts'})
            away_snap_counts = html_to_pandas(away_snap_counts_html)
            away_snap_counts.columns = cols
            away_snap_counts.drop(index=[0, 1], inplace=True)
            away_snap_counts['team'] = 'away'
            snap_counts = pd.concat([home_snap_counts, away_snap_counts])
            self._snap_counts = snap_counts
            self._logger.info(f'Player snap counts data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Player snap counts data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_drives(self):
        """Scrape the drives data for the game and save it as a pandas dataframe"""
        try:
            home_drives_html = self._html.find('table', {'id': 'home_drives'})
            home_drives = html_to_pandas(home_drives_html)
            home_drives.columns = home_drives.iloc[0]
            home_drives.drop(index=0, inplace=True)
            home_drives['team'] = 'home'
            away_drives_html = self._html.find('table', {'id': 'vis_drives'})
            away_drives = html_to_pandas(away_drives_html)
            away_drives.columns = away_drives.iloc[0]
            away_drives.drop(index=0, inplace=True)
            away_drives['team'] = 'away'
            drives = pd.concat([home_drives, away_drives])
            drives.rename(columns={'#': 'drive_num'}, inplace=True)
            self._drives = drives
            self._logger.info(f'Drives data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Drives data data was not scraped for the game {self._id}')
            self._logger.error(e)

    def _scrape_play_by_play(self):
        """Scrape the play by play data for the game and save it as a pandas dataframe"""
        try:
            play_by_play_html = self._html.find('table', {'id': 'pbp'})
            play_by_play = html_to_pandas(play_by_play_html)
            play_by_play.columns = play_by_play.iloc[0]
            play_by_play = play_by_play[play_by_play['Quarter'].isin(['1', '2', '3', '4', 'OT'])]
            self._play_by_play = play_by_play
            self._logger.info(f'Play by play data scraped for the game {self._id}')
        except Exception as e:
            self._logger.error(f'Play by play data was not scraped for the game {self._id}')
            self._logger.error(e)

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
        saves = [self.get_game_info().to_csv(filepath + self.get_id() + '_game_info.csv'),
                 self.get_officials().to_csv(filepath + self.get_id() + '_officials.csv'),
                 self.get_team_stats().to_csv(filepath + self.get_id() + '_team_stats.csv'),
                 self.get_pass_rush_receive().to_csv(filepath + self.get_id() + '_pass_rush_receive.csv'),
                 self.get_defense().to_csv(filepath + self.get_id() + '_defense.csv'),
                 self.get_kick_punt_return().to_csv(filepath + self.get_id() + '_kick_punt_return.csv'),
                 self.get_kicking_punting().to_csv(filepath + self.get_id() + '_kicking_punting.csv'),
                 self.get_advanced_passing().to_csv(filepath + self.get_id() + '_advanced_passing.csv'),
                 self.get_advanced_rushing().to_csv(filepath + self.get_id() + '_advanced_rushing.csv'),
                 self.get_advanced_receiving().to_csv(filepath + self.get_id() + '_advanced_receiving.csv'),
                 self.get_advanced_defense().to_csv(filepath + self.get_id() + '_advanced_defense.csv'),
                 self.get_starters().to_csv(filepath + self.get_id() + '_starters.csv'),
                 self.get_snap_counts().to_csv(filepath + self.get_id() + '_snap_counts.csv'),
                 self.get_drives().to_csv(filepath + self.get_id() + '_drives.csv'),
                 self.get_play_by_play().to_csv(filepath + self.get_id() + '_play_by_play.csv')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self._id} as CSV files")

    def save_parquet(self, filepath):
        saves = [self.get_game_info().to_parquet(filepath + self.get_id() + '_game_info.parquet'),
                 self.get_officials().to_parquet(filepath + self.get_id() + '_officials.parquet'),
                 self.get_team_stats().to_parquet(filepath + self.get_id() + '_team_stats.parquet'),
                 self.get_pass_rush_receive().to_parquet(filepath + self.get_id() + '_pass_rush_receive.parquet'),
                 self.get_defense().to_parquet(filepath + self.get_id() + '_defense.parquet'),
                 self.get_kick_punt_return().to_parquet(filepath + self.get_id() + '_kick_punt_return.parquet'),
                 self.get_kicking_punting().to_parquet(filepath + self.get_id() + '_kicking_punting.parquet'),
                 self.get_advanced_passing().to_parquet(filepath + self.get_id() + '_advanced_passing.parquet'),
                 self.get_advanced_rushing().to_parquet(filepath + self.get_id() + '_advanced_rushing.parquet'),
                 self.get_advanced_receiving().to_parquet(filepath + self.get_id() + '_advanced_receiving.parquet'),
                 self.get_advanced_defense().to_parquet(filepath + self.get_id() + '_advanced_defense.parquet'),
                 self.get_starters().to_parquet(filepath + self.get_id() + '_starters.parquet'),
                 self.get_snap_counts().to_parquet(filepath + self.get_id() + '_snap_counts.parquet'),
                 self.get_drives().to_parquet(filepath + self.get_id() + '_drives.parquet'),
                 self.get_play_by_play().to_parquet(filepath + self.get_id() + '_play_by_play.parquet')]
        for s in saves:
            try:
                s
            except Exception as e:
                self._logger.warning(f'Exception saving data: {e}')
        self._logger.info(f"Data saved for game: {self._id} as parquet files")


# %%
class NFLYearScraper:
    """
    desc

    Attributes:

    Methods:

    """
    # TODO: need to add functionality to scrape injuries, travel, draft, combine, coaches and players

    def __init__(self, year, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_year(year)
        self.weeks = list()
        self._scraper_proxy = scraper_proxy
        self._logger.info(f"Created year object for: {str(self.year)}")

    # Setters
    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()

    def scrape_year(self):
        self._logger.info(f"Scraping data for year: {str(self.year)}")
        for w in WEEKS:
            self.weeks.append(NFLWeekScraper(
                year=self.year,
                week=w,
                scraper_proxy=self._scraper_proxy
            ))
        random.shuffle(self.weeks)
        for w in self.weeks:
            w.scrape_week()

    def scrape_weeks(self):
        self._logger.info(f"Scraping all of the weeks in the year: {str(self.year)}")
        for w in self.weeks:
            w.scrape_games()

    def save_year_data(self):
        self._logger.info(f"Saving all of the raw data for the year: {str(self.year)}")
        for w in self.weeks:
            w.save_week_data()


# %%
class NFLWeekScraper:
    """
    description

    Attributes:

    Methods:

    """
    # TODO: need to add functionality to scrape injuries, travel, coaches and players
    base_url = 'https://www.pro-football-reference.com/years/'

    def __init__(self, year, week, scraper_proxy):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._set_year(year)
        self._set_week(week)
        self._scraper_proxy = scraper_proxy
        self._html = None
        self.games = list()
        self._logger.info(f"Created week object for: {self.year}, {self.week}")

    # Setters
    def _set_year(self, year):
        if check_year(year):
            self.year = year
        else:
            raise ValueError()  # TODO: better error handling

    def _set_week(self, week):
        if week in WEEKS:
            self.week = week
        else:
            raise ValueError()  # TODO: better error handling

    # Methods
    def scrape_week(self):
        self._logger.info(f"Scraping week data from: {str(self.year) + '/' + self.week + '.htm'}")
        self._html = BeautifulSoup(comm.sub('', self._scraper_proxy.get(self.base_url + str(self.year) + '/' + self.week
                                                                        + '.htm').text), 'lxml')
        for g in self._html.find_all("div", {"class": "game_summary"}):
            self.games.append(NFLGameScraper(
                year=self.year,
                week=self.week,
                link=g.find('td', {'class': 'gamelink'}).find('a', href=True)['href'],
                scraper_proxy=self._scraper_proxy
            ))
        random.shuffle(self.games)

    def scrape_games(self):
        self._logger.info(f"Scraping game data for week: {self.year}, {self.week}")
        # scramble the list of games before scraping them
        for g in self.games:
            g.scrape_game()

    def save_week_data(self):
        self._logger.info(f"Saving raw game data for week: {self.year}, {self.week}")
        for g in self.games:
            filepath = f'./data/raw/games/{g.get_id()}/'
            if not os.path.isdir(filepath):
                os.mkdir(filepath)
            g.save('csv', filepath)
