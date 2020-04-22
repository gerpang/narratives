#!/usr/bin/env python3
""" Module-wide constants"""

# Wait time between AO3 requests in seconds
DELAY = 4

# File name of output file
OUTPUT_FILE = 'work_id_list.txt'

# Location of raw data dumps. Fandom subdirectories will be located here
DATA_PATH = '../data/raw/'

KUDO_PREFIX = 'kudos'
META_PREFIX = 'meta'
LOG_SUFFIX = '.log'
DATA_SUFFIX = '.csv'

# HTTP Request Headers
HTTP_HEADERS = {'User-Agent':
                'Scraping meta for fan analysis; rebecca.sanjabi@gmail.com'}

# When testing a single fandom
TEST_FANDOM = 'Star Wars: The Clone Wars (2008) - All Media Types'
# TEST_FANDOM = 'Overwatch (Video Game)'

# How many attempts at requesting page before quitting
MAX_ERRORS = 3