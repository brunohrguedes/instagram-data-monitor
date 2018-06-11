#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import codecs
import configparser
import errno
import glob
from operator import itemgetter
import json
import logging.config
import hashlib
import os
import re
import sys
import textwrap
import time

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import warnings

import threading
import concurrent.futures
import requests
import tqdm

from constants import *
from datetime import datetime



class InstagramScraper(object):
    """InstagramScraper scrapes and downloads an instagram user's photos and videos"""

    def __init__(self, **kwargs):
        default_attr = dict(username='', usernames=[], filename=None,
                            login_user=None, login_pass=None,
                            destination='./', retain_username=False, interactive=False,
                            quiet=False, maximum=0, media_metadata=False, latest=False,
                            latest_stamps=False,
                            media_types=['image', 'video', 'story-image', 'story-video'],
                            tag=False, location=False, search_location=False, comments=False,
                            verbose=0, include_location=False, filter=None)

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        # story media type means story-image & story-video
        if 'story' in self.media_types:
            self.media_types.remove('story')
            if 'story-image' not in self.media_types:
                self.media_types.append('story-image')
            if 'story-video' not in self.media_types:
                self.media_types.append('story-video')

        # Read latest_stamps file with ConfigParser
        self.latest_stamps_parser = None
        if self.latest_stamps:
            parser = configparser.ConfigParser()
            parser.read(self.latest_stamps)
            self.latest_stamps_parser = parser
            # If we have a latest_stamps file, latest must be true as it's the common flag
            self.latest = True

        # Set up a logger
        self.logger = InstagramScraper.get_logger(level=logging.DEBUG, verbose=default_attr.get('verbose'))

        self.posts = []
        self.session = requests.Session()
        self.session.headers = {'user-agent': CHROME_WIN_UA}
        self.session.cookies.set('ig_pr', '1')
        self.rhx_gis = None

        self.cookies = None
        self.logged_in = False
        self.last_scraped_filemtime = 0
        if default_attr['filter']:
            self.filter = list(self.filter)

        self.quit = False

        
    def safe_get(self, *args, **kwargs):
        # out of the box solution
        # session.mount('https://', HTTPAdapter(max_retries=...))
        # only covers failed DNS lookups, socket connections and connection timeouts
        # It doesnt work when server terminate connection while response is downloaded
        retry = 0
        retry_delay = RETRY_DELAY
        while True:
            if self.quit:
                return
            try:
                response = self.session.get(timeout=CONNECT_TIMEOUT, *args, **kwargs)
                if response.status_code == 404:
                    return
                response.raise_for_status()
                content_length = response.headers.get('Content-Length')
                if content_length is None or len(response.content) != int(content_length):
                    #if content_length is None we repeat anyway to get size and be confident
                    raise PartialContentException('Partial response')
                return response
            except (KeyboardInterrupt):
                raise
    
    def get_json(self, *args, **kwargs):
        """Retrieve text from url. Return text as string or None if no data present """
        resp = self.safe_get(*args, **kwargs)

        if resp is not None:
            return resp.text

    def login(self):
        """Logs in to instagram."""
        self.session.headers.update({'Referer': BASE_URL})
        req = self.session.get(BASE_URL)

        self.session.headers.update({'X-CSRFToken': req.cookies['csrftoken']})

        login_data = {'username': self.login_user, 'password': self.login_pass}
        login = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.cookies = login.cookies
        login_text = json.loads(login.text)

        if login_text.get('authenticated') and login.status_code == 200:
            self.logged_in = True
            self.rhx_gis = self.get_shared_data()['rhx_gis']
        else:
            self.logger.error('Login failed for ' + self.login_user)


    def logout(self):
        """Logs out of instagram."""
        if self.logged_in:
            try:
                logout_data = {'csrfmiddlewaretoken': self.cookies['csrftoken']}
                self.session.post(LOGOUT_URL, data=logout_data)
                self.logged_in = False
            except requests.exceptions.RequestException:
                self.logger.warning('Failed to log out ' + self.login_user)



    def get_last_scraped_filemtime(self, dst):
        """Stores the last modified time of newest file in a directory."""
        list_of_files = []
        file_types = ('*.jpg', '*.mp4')

        for type in file_types:
            list_of_files.extend(glob.glob(dst + '/' + type))

        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getmtime)
            return int(os.path.getmtime(latest_file))
        return 0


    def scrape(self, file , folder='../../Dados/stories/csv/'):
        """Crawls through and downloads user's media"""
        agora = datetime.now()
        data = str(agora.day)+'-'+str(agora.month)+'-'+str(agora.year)
        
        # if not os.path.exists('stories'):
        #     os.makedirs('stories')

        if not os.path.exists('csv'):    # Pasta para os csv
            os.makedirs('csv')            

        if file =='':
            file = folder + 'stories' +data+'.csv'

        else:
            file=folder + file + '.csv'

        try:
            arquivo = open(file, 'a')
            arquivo.write('username'+';'+'Data'+';'+'stories'+'\n')
            arquivo.close()
            for username in self.usernames:
                self.posts = []
                self.last_scraped_filemtime = 0
                greatest_timestamp = 0
                future_to_item = {}

                dst = file

                # Get the user metadata.
                shared_data = self.get_shared_data(username)
                user = self.deep_get(shared_data, 'entry_data.ProfilePage[0].graphql.user')
                if user is None:
                    print ('instagram'+' '+ username+' ' +'não existe'+'\n')
                else:
                    self.get_stories(dst, future_to_item, user, username)
        finally:
            self.quit = True
            self.logout()            

    def get_stories(self, dst, future_to_item, user, username):
        """Scrapes the user's stories."""
        if self.logged_in and \
                ('story-image' in self.media_types or 'story-video' in self.media_types):
            # Get the user's stories.
            #print (user['id'])
            if user['id'] is not None:
                stories = self.fetch_stories(user['id'])
                iter = tqdm.tqdm(stories, desc='{0} stories'.format(username), unit=" media")
                print(iter.total)

            agora = datetime.now()

            arquivo = open('./'+dst, 'a')

            arquivo.write(username+';'+str(agora.day)+'/'+str(agora.month)+'/'+str(agora.year)+'-'+
            	str(agora.hour)+':'+str(agora.minute)+';'+str(iter.total)+'\n')
            arquivo.close()

    def get_shared_data(self, username=''):
        """Fetches the user's metadata."""
        resp = self.get_json(BASE_URL + username)

        if resp is not None and '_sharedData' in resp:
            try:
                shared_data = resp.split("window._sharedData = ")[1].split(";</script>")[0]
                return json.loads(shared_data)
            except (TypeError, KeyError, IndexError):
                pass

    def fetch_stories(self, user_id):
        """Fetches the user's stories."""
        resp = self.get_json(STORIES_URL.format(user_id), headers={
            'user-agent': STORIES_UA,
            'cookie': STORIES_COOKIE.format(self.cookies['ds_user_id'], self.cookies['sessionid'])
        })

        if resp is not None:
            retval = json.loads(resp)
            if retval['reel'] and 'items' in retval['reel'] and len(retval['reel']['items']) > 0:
                return [self.set_story_url(item) for item in retval['reel']['items']]

        return []
    def set_story_url(self, item):
        """Sets the story url."""
        urls = []
        if 'video_versions' in item:
            urls.append(item['video_versions'][0]['url'])
        if 'image_versions2' in item:
            urls.append(item['image_versions2']['candidates'][0]['url'].split('?')[0])
        item['urls'] = urls
        return item


    @staticmethod
    def get_logger(level=logging.DEBUG, verbose=0):
        """Returns a logger."""
        logger = logging.getLogger(__name__)

        fh = logging.FileHandler('instagram-scraper.log', 'w')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        fh.setLevel(level)
        logger.addHandler(fh)

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        sh_lvls = [logging.ERROR, logging.WARNING, logging.INFO]
        sh.setLevel(sh_lvls[verbose])
        logger.addHandler(sh)
        
        logger.setLevel(level)

        return logger


    @staticmethod
    def parse_delimited_str(input):
        """Parse the string input as a list of delimited tokens."""
        return re.findall(r'[^,;\s]+', input)

    def deep_get(self, dict, path):
        def _split_indexes(key):
            split_array_index = re.compile(r'[.\[\]]+')  # ['foo', '0']
            return filter(None, split_array_index.split(key))

        ends_with_index = re.compile(r'\[(.*?)\]$')  # foo[0]

        keylist = path.split('.')

        val = dict

        for key in keylist:
            try:
                if ends_with_index.search(key):
                    for prop in _split_indexes(key):
                        if prop.isdigit():
                            val = val[int(prop)]
                        else:
                            val = val[prop]
                else:
                    val = val[key]
            except (KeyError, IndexError, TypeError):
                return None

        return val


    @staticmethod
    def parse_file_usernames(usernames_file):
        """Parses a file containing a list of usernames."""
        users = []

        
        with open(usernames_file) as user_file:
            for line in user_file.readlines():
                # Find all usernames delimited by ,; or whitespace
                users += re.findall(r'[^,;\s]+', line.split("#")[0])

        return users

def main():
    args = argparse.ArgumentParser()
    file = input('digite o nome do arquivo que deseja salvar os dados'+'\n'+'(se deixar em branco será gerado um arquivo com data e hora da coleta):'+'\n')
    args.add_argument('username')
    args.add_argument('--login-user', '--login_user', '-u')
    args.add_argument('--login-pass', '--login_pass', '-p')
    args.add_argument('--filename', '-f')
  
    args.filename = 'ig_users.txt'
    args.login_user = 'instagramagile@gmail.com'
    args.login_pass = 'instagramagile12018'
    args.usernames = InstagramScraper.parse_file_usernames(args.filename)
    scraper = InstagramScraper(**vars(args))
    scraper.login()
    scraper.scrape(file)


if __name__ == '__main__':
    main()

