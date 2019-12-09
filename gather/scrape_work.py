# script to scrape data from AO3
from gather.ao3structures import Work
from bs4 import BeautifulSoup
import progressbar
import urllib.request
import urllib.parse
import math 
import time
import sys
import json

class PageScraper():
    def __init__(self, id):
        self.url = "https://archiveofourown.org/works/" + str(id) + "?view_adult=true&amp;view_full_work=true"
        self.fanWork = Work(id, self.url)

    def print(self):
        self.fanWork.print()
        
    def scrape(self):
        ''' Scrapes the contents of the page '''
        
        try:
            with urllib.request.urlopen(self.url) as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
        except:
            print("Error reading works page. ", self.url)
            return

        self.fanWork.rating = self._get_rating(soup)
        self.fanWork.archive_warnings = self._get_warning(soup)
        self.fanWork.categories = self._get_categories(soup)
        self.fanWork.fandoms = self._get_fandoms(soup)
        self.fanWork.relationships = self._get_relationships(soup)
        self.fanWork.characters = self._get_characters(soup)
        self.fanWork.additional_tags = self._get_additional_tags(soup)
        self.fanWork.language = self._get_language(soup)
        self.fanWork.published = self._get_published(soup)
        self.fanWork.updated = self._get_updated(soup)
        self.fanWork.words = self._get_words(soup)
        self.fanWork.chapter_current_count, self.fanWork.chapter_max_count = self._get_chapter_count(soup)
        self.fanWork.comments_count = self._get_comments_count(soup) # TODO ERROR (OR MAYBE NOT?)
        self.fanWork.kudos_count = self._get_kudos_count(soup)  
        self.fanWork.bookmarks_count = self._get_bookmarks_count(soup)
        self.fanWork.hits = self._get_hits_count(soup)
        self.fanWork.author_pseud, self.fanWork.author_user = self._get_author(soup)
        self.fanWork.title = self._get_title(soup)

        # Crawl to kudos page
        kudos_url = "https://archiveofourown.org/works/" + str(self.fanWork.id) + "/kudos"
        try:

            with urllib.request.urlopen(kudos_url) as f:
                kudo_soup = BeautifulSoup(f.read().decode('utf-8'), features="lxml")
                self.fanWork.kudo_guest_count, self.fanWork.kudos_users = self._get_kudos(kudo_soup)
        except:
            print("Error reading kudos page.", kudos_url)
        
        # Crawl comments
        pass

        # Crawl bookmarks
        "https://archiveofourown.org/works/14388135/bookmarks"
        pass


    def _get_rating(self, soup):
        # Get one rating back
        try:
            return soup.find_all(class_="rating tags")[1].get_text().strip()
        except:
            print("Error grabbing rating.")

    def _get_warning(self, soup):
        # Get a list of warnings
        try:
            warnings = soup.find_all(class_="warning tags")[1].find_all('li')
            warning_list = [warning.get_text().strip() for warning in warnings]
            return warning_list
        except:
            print("Error grabbing archive warnings.")
            return

    def _get_categories(self, soup):
        # Get a list of (relationship) categories
        try:
            categories = soup.find_all(class_="category tags")[1].find_all('li')
            category_list = [category.get_text().strip() for category in categories]
            return category_list
        except:
            print("Error grabbing categories.")
            return

    def _get_fandoms(self, soup):
        # Get a list of fandoms
        try:
            fandoms = soup.find_all(class_="fandom tags")[1].find_all('li')
            fandom_list = [fandom.get_text().strip() for fandom in fandoms]
            return fandom_list
        except:
            print("Error grabbing fandoms.")
            return

    def _get_relationships(self, soup):
        # Get a list of relationships
        try:
            ships = soup.find_all(class_="relationship tags")[1].find_all('li')
            ship_list = [ship.get_text().strip() for ship in ships]
            return ship_list
        except:
            print("Error grabbing relationships.")
            return

    def _get_characters(self, soup):
        # Get a list of characters
        try:
            characters = soup.find_all(class_="character tags")[1].find_all('li')
            char_list = [char.get_text().strip() for char in characters]
            return char_list
        except:
            print("Error grabbing characters.")
            return

    def _get_additional_tags(self, soup):
        # Get a list of additional tags
        try:
            add_tags = soup.find_all(class_="freeform tags")[1].find_all('li')
            add_tag_list = [tag.get_text().strip() for tag in add_tags]
            return add_tag_list
        except:
            print("Error grabbing additional tags.")
            return

    def _get_language(self, soup):
        # Get language
        try:
            return soup.find_all(class_="language")[1].get_text().strip()
        except:
            print("Error grabbing language.")

    def _get_published(self, soup):
        # Get published date 
        try:
            return soup.find_all(class_="published")[1].get_text().strip()
        except:
            print("Error grabbing published date.")

    def _get_updated(self, soup): # optional
        # Get updated date 
        try:
            return soup.find_all(class_="status")[1].get_text().strip()
        except:
            print("Error grabbing updated date.")

    def _get_words(self, soup):
        # Get word count  
        try:
            return soup.find_all(class_="words")[1].get_text().strip()
        except:
            print("Error grabbing word count.")

    def _get_chapter_count(self, soup):
        # Get chapters
        # TODO how to deal with single chapters 
        try:
            chapters = soup.find_all(class_="chapters")[1].get_text().strip()
            current,total = chapters.split('/')
            return current, total
        except:
            print("Error grabbing published date.")

    def _get_comments_count(self, soup):
        # Get total comments 
        try:
            return soup.find_all(class_="comments")[2].get_text().strip()
        except:
            print("Error grabbing total comment count.")

    def _get_kudos_count(self, soup):
        # Get total kudos count 
        try:
            return soup.find_all(class_="kudos")[1].get_text().strip()
        except:
            print("Error grabbing total kudos count.")

    def _get_bookmarks_count(self, soup):
        # Get total bookmarks 
        try:
            return soup.find_all(class_="bookmarks")[1].get_text().strip()
        except:
            print("Error grabbing total bookmark count.")

    def _get_hits_count(self, soup):
        # Get total hits 
        try:
            return soup.find_all(class_="hits")[1].get_text().strip()
        except:
            print("Error grabbing total hits count.")

    def _get_title(self, soup):
        # Get title 
        try:
            return soup.find(class_="title heading").get_text().strip()
        except:
            print("Error grabbing title.")

    def _get_author(self, soup):
        # Get author 
        psued = ''
        primary = ''
        try:
            user_entire = soup.find(class_="byline heading").get_text().strip()
            if ' ' in user_entire:
                psued, primary = user_entire.split()
                primary = primary.lstrip('(').rstrip(')')
            return psued, primary
        except:
            print("Error grabbing author.")

    def _get_kudos(self, soup):
        # Get list of users who gave kudos and number of guests who kudo'd

        try:
            user_list_soup = soup.find(class_="kudos")
            _, guest_text = user_list_soup.get_text().split('as well as')
            guest_count = guest_text.replace('\n', '').strip().rstrip('guests left kudos on this work!')
            kudo_names = [user.get_text() for user in user_list_soup.find_all('a')]
            return guest_count, kudo_names
        except:
            print("Error grabbing title.")
            return '', ''




