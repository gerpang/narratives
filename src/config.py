#!/usr/bin/env python3
""" Module-wide constants"""


import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Wait time between AO3 requests in seconds
DELAY = 5

# Location of raw data dumps. Fandom subdirectories will be located here
DATA_PATH = '../data/raw/'
MODEL_PATH = '../models/'

INDICES_PREFIX = 'indices'
MODEL_PREFIX = 'implicit'
KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'
META_DB_PREFIX = 'meta_db'

LOG_SUFFIX = '.log'
DATA_SUFFIX = '.csv'
PICKLE_SUFFIX = '.pkl'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

# DELETE ME

# When testing a single fandom
TEST_FANDOM = 'The Mandalorian (TV)'
# TEST_FANDOM_LIST = ['The Mandalorian (TV)',
TEST_FANDOM_LIST = ['Star Wars: A New Dawn - John Jackson Miller']
'''
                    'Star Wars: Kanan (Comics)']
                    'Star Wars: A New Dawn - John Jackson Miller',
                    'Star Wars: Kanan (Comics)',
                    'Star Wars: Thrawn Series - Timothy Zahn (2017)',
                    'Star Wars Original Trilogy',
                    'Star Wars: The Clone Wars (2008) - All Media Types'
                    ]
'''

# How many attempts at requesting page before quitting
MAX_ERRORS = 3

HOST = 'ec2-18-233-32-61.compute-1.amazonaws.com'

META_COLS = ['work_id', 'title', 'author', 'gifted', 'rating', 'warnings',
             'category', 'status', 'fandom', 'relationship', 'character',
             'additional_tags', 'summary', 'language', 'words', 'chapters',
             'collections', 'comments', 'kudos', 'bookmarks', 'hits',
             'series_part', 'series_name', 'updated', 'scrape_date']
