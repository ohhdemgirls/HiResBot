import os
import sys
import time
import praw
from pprint import pprint
from PIL import Image

__author__ = 'Ben and Daniel'
__version__ = '0.0.1'

class RedditBot(object):

    def __init__(self, uname, passwd):
        self.api = praw.Reddit(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0')     # Change 'SadiqBot' to your bot's name
        self.input = raw_input("What subreddit would you like to run on? ")
        self.subreddit = self.api.get_subreddit(self.input)

    def check_higher_res(self, url):
        im = Image.open(url)
        dpi = im.info['dpi']
        return dpi

    def upload_new(self):
         #upload_image(self.subreddit, image_path, name=None, header=False)
         pass

    def start(self):
        while True:
            # get links from subreddit we are interested in
            for submission in self.subreddit.get_hot(limit=10):
                check_higher_res(submission.url)

            #call check_higher_res
            #call upload_new

            time.sleep(1800)


def main():
    bot = RedditBot('HiResBot', 'crazychickenbaloons') # Change 'user' and 'pass' to your login info
    try:
        bot.start()
    except:
        raise

    return 0

if __name__ == '__main__':
    main()