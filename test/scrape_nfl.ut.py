#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for the scrape_nfl.py file.

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

# Imports
import unittest
from data_scraping.scrape_nfl import *
import pandas as pd


# Load data for testing
def load_testing_html():
    with open('test_data/test_html.txt', 'r') as f:
        return f.read()


def load_testing_data():
    return pd.read_csv()


# Tests
class TestHtmlToPandas(unittest.TestCase):
    """
    Unit Tests for the html_to_pandas function.
    """
    html_for_testing = load_testing_html
    dataframe_for_testing = pd.DataFrame()

    def test_output(self):
        self.assertIsInstance(html_to_pandas(self.html_for_testing), pd.DataFrame)


class TestNFLDraftScraper(unittest.TestCase):
    """
    Unit tests for the NFLDraftScraper class.
    """
    test_data = load_testing_html

    def test(self):
        self.assertIsInstance()


class TestNFLCombineScraper(unittest.TestCase):
    """
    Unit tests for the NFLCombineScraper class.
    """
    test_data = load_testing_html

    def test(self):
        self.assertIsInstance()


class TestNFLYearScraper(unittest.TestCase):
    """
    Unit tests for the NFLYearScraper class.
    """
    test_data = load_testing_html

    def test(self):
        self.assertIsInstance()


class TestNFLWeekScraper(unittest.TestCase):
    """
    Unit tests for the NFLWeekScraper class.
    """
    test_data = load_testing_html

    def test(self):
        self.assertIsInstance()


class TestNFLGameScraper(unittest.TestCase):
    """
    Unit tests for the NFLGameScraper class.
    """
    test_data = load_testing_html

    def test(self):
        self.assertIsInstance()
