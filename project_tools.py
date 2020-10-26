#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic Data Science tools used throughout the project.

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

#%%
import pandas as pd
import numpy as np
import random
import requests
from configparser import ConfigParser
import time
import sqlalchemy
import pymysql

#%%
def expand_pandas_output():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


#%%
def calculate_psi(expected, actual, buckettype='bins', buckets=10, axis=0):
    """Calculate the PSI (population stability index) across all variables
    example: calculate_psi(initial, new, buckettype='quantiles', buckets=10, axis=1)

    Args:
       expected: numpy matrix of original values
       actual: numpy matrix of new values, same size as expected
       buckettype: type of strategy for creating buckets, bins splits into even splits, quantiles splits into quantile buckets
       buckets: number of quantiles to use in bucketing variables
       axis: axis by which variables are defined, 0 for vertical, 1 for horizontal
    Returns:
       psi_values: ndarray of psi values for each variable
    Author:
       Matthew Burke
       github.com/mwburke
       worksofchart.com
    """

    def psi(expected_array, actual_array, buckets):
        """Calculate the PSI for a single variable
        Args:
           expected_array: numpy array of original values
           actual_array: numpy array of new values, same size as expected
           buckets: number of percentile ranges to bucket the values into
        Returns:
           psi_value: calculated PSI value
        """

        def scale_range(input, min, max):
            input += -(np.min(input))
            input /= np.max(input) / (max - min)
            input += min
            return input

        breakpoints = np.arange(0, buckets + 1) / buckets * 100

        if buckettype == 'bins':
            breakpoints = scale_range(breakpoints, np.min(expected_array), np.max(expected_array))
        elif buckettype == 'quantiles':
            breakpoints = np.stack([np.percentile(expected_array, b) for b in breakpoints])

        expected_percents = np.histogram(expected_array, breakpoints)[0] / len(expected_array)
        actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)

        def sub_psi(e_perc, a_perc):
            """Calculate the actual PSI value from comparing the values.
               Update the actual value to a very small number if equal to zero
            """
            if a_perc == 0:
                a_perc = 0.0001
            if e_perc == 0:
                e_perc = 0.0001

            value = (e_perc - a_perc) * np.log(e_perc / a_perc)
            return value

        psi_value = np.sum(sub_psi(expected_percents[i], actual_percents[i]) for i in range(0, len(expected_percents)))

        return psi_value

    if len(expected.shape) == 1:
        psi_values = np.empty(len(expected.shape))
    else:
        psi_values = np.empty(expected.shape[axis])

    for i in range(0, len(psi_values)):
        if len(psi_values) == 1:
            psi_values = psi(expected, actual, buckets)
        elif axis == 0:
            psi_values[i] = psi(expected[:,i], actual[:,i], buckets)
        elif axis == 1:
            psi_values[i] = psi(expected[i,:], actual[i,:], buckets)

    return psi_values


#%%
def connect_to_db():
    parser = ConfigParser()
    parser.read('config.ini')
    user = parser.get('mariadb', 'user')
    pswd = parser.get('mariadb', 'password')
    host = parser.get('mariadb', 'host')
    db = parser.get('mariadb', 'database')
    return sqlalchemy.create_engine(f"mysql+pymysql://{user}:{pswd}@{host}/{db}", echo=True)


#%%
class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)


#%%
class ScraperProxy:
    """
    A Class to use the request library alongside proxies from webshare. More infromation about webshare can be found
    at https://proxy.webshare.io/docs/?python#introduction. Future plans include implementation of session logic.

    Requires a config.ini file that has a section header [webshare] with an api_key in the section.

    Attributes:
        _proxies: list of proxies - private.
        _api_key:

    Methods:
        _get_proxies: Get the avaliable proxies from webshare.
        _try_get_request: A meth
        get_with_proxy:

    """

    def __init__(self):
        self._proxies = []
        parser = ConfigParser()
        parser.read('config.ini')
        self._api_key = parser.get('webshare','api_key')
        self._get_proxies()

    def _get_proxies(self):
        response = requests.get('https://proxy.webshare.io/api/proxy/list/',
                                headers={"Authorization": f"Token {self._api_key}"})
        for r in response.json()['results']:
            if r['valid']:
                user = r['username']
                pswd = r['password']
                ip = r['proxy_address']
                port = r['ports']['http']
                self._proxies.append({
                    'http': f'http://{user}:{pswd}@{ip}:{port}/',
                    'https': f'https://{user}:{pswd}@{ip}:{port}/'
                })

    def _try_get_request(self, url, proxy):
        time.sleep(random.random() * 2 + 1)
        response = requests.get(url, proxies=proxy)
        if 200 <= response.status_code <= 299:
            return response
        if 400 <= response.status_code <= 499:
            return 'Client HTTP Error'
        if 500 <= response.status_code <= 599:
            return 'Server HTTP Error'
        else:
            return 'Other HTTP Error'

    def get(self, url):
        if len(self._proxies) == 0:
            self._get_proxies()
        proxy = self._proxies[random.randint(0, len(self._proxies) - 1)]
        try:
            response = self._try_get_request(url, proxy)
            if response == 'Client HTTP Error':
                # Assume the proxy is bad and move on
                raise SystemError('Bad Proxy')
            elif response == 'Server HTTP Error':
                # Try Again
                self.get(url)
            elif response == 'Other HTTP Error':
                # Try Again
                self.get(url)
            else:
                return response
        except Exception as e:
            # log the exception here
            print(e)
            try:
                # implement here what to do when there’s a connection error
                # remove the used proxy from the pool and retry the request using another one
                self._proxies.remove(proxy)
                self.get(url)
            except Exception as e:
                raise e
