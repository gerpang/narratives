# Class defining work data structure
import urllib
from datetime import datetime
import json
import pytz

class Work:
    def __init__(self, id, url):
        ''' Constructor for this class. '''
        # Create some member animals
        self.id = id
        self.url = url
        self.rating = ''
        self.archive_warnings = []
        self.categories = []
        self.fandoms = []
        self.relationships = []
        self.characters = []
        self.additional_tags = []
        self.language = ''
        self.published = ''
        self.updated = ''
        self.words = ''
        self.chapter_current_count = ''
        self.chapter_max_count = ''
        self.comments_count = ''
        self.comments = []
        self.kudos_total_count = ''
        self.kudo_guest_count = ''
        self.kudos_users = []
        self.bookmarks_count = ''
        self.hits = ''
        self.scrape_date = str(datetime.now(tz=pytz.utc))
        self.meta_notes = {}    # a  dict {'all': Chapter, '1': Chapter, 'end': Chapter}
        self.author_pseud = ''        # user/pseud
        self.author_user = ''    # user/primary
        self.title = ''
        self.body_non_text = '' # detects things like links or images
        self.gift = ''          # User(s) work was gifted for
        self.series = ''
        self.collections = ''

    def print(self):
        print(json.dumps(vars(self), sort_keys=True, indent=4))

class Chapter:
    def __init__(self, title, summary, notes, body):
        self.title = title
        self.summary = summary
        self.notes = notes
        self.body = body

class Comment:
    def __init__(self, user, chapter_num, date_time, comment_text, reply_to):
        self.user = user 
        self.chapter_num = chapter_num
        self.date_time = date_time
        self.comment_text = comment_text
        self.reply_to = reply_to

class Bookmark:
    def __init__(self, user, date, tags, comments):
        self.user = user 
        self.tags = tags
        self.date = date
        self.comments = comments

class Search:
    def __init__(self, type_of, config):
        self.type_of = type_of
        self.params = config

    def generateURL(self, page=1):
        # generate urls

        self.params['page'] = page
        params = urllib.parse.urlencode(self.params)
        url = "https://archiveofourown.org/" + self.type_of + "?%s" % params

        return url
