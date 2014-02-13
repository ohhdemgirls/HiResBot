import re, praw, requests, os, glob, sys, time, urllib, ImageFile
from BeautifulSoup import BeautifulSoup

__author__ = 'Ben and Daniel'
__version__ = '0.0.1'

class RedditBot(object):

    def __init__(self, uname, passwd):
        # Identify with name of bot
        self.api = praw.Reddit(user_agent='HiResBot')
        # Which subreddit to run on -- Temp for now, we'll handle this better that rawinput
        self.input = raw_input("What subreddit would you like to run on? ")
        self.subreddit = self.api.get_subreddit(self.input)
        # Some regex
        self.imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')

    def upload_new(self):
         #self.api.upload_image(self.subreddit, image_path, name=None, header=False)
         #Aren't we just going to post a comment! This would make a post!
         pass 
        
    def checkHigherRes(self, imageUrl):
        imgRes = self.getsizes(imageUrl)
        if imgRes[0] < 640: # Less than 480p
            print imageUrl +", Not HD"
        else:
            print imageUrl +", HD"
    
    def getsizes(self, uri): # Blatantly stolen from http://effbot.org/zone/pil-image-size.htm
        # get file size *and* image size (None if not known)
        file = urllib.urlopen(uri)
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return p.image.size
                break
        file.close()
        return None

    def start(self):
        while True:
            # Get links from subreddit we are interested in
            for submission in self.subreddit.get_hot(limit=10):
                # Check for the cases where we will skip a submission:
                if "imgur.com/" not in submission.url:
                    continue # skip non-imgur submissions
                if 'http://imgur.com/a/' in submission.url:
                    # This is an album submission.
                    albumId = submission.url[len('http://imgur.com/a/'):]
                    htmlSource = requests.get(submission.url).text

                    soup = BeautifulSoup(htmlSource)
                    try:
                        matches = soup.select('.album-view-image-link a')
                        for match in matches:
                            imageUrl = match['href']
                            if '?' in imageUrl:
                                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
                            else:
                                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
                            self.checkHigherRes('http:' + match['href'])
                    except Exception as e:
                        print e.message

                elif 'http://i.imgur.com/' in submission.url:
                    # The URL is a direct link to the image.
                    mo = self.imgurUrlPattern.search(submission.url) # using regex here instead of BeautifulSoup because we are pasing a url, not html

                    imgurFilename = mo.group(2)
                    if '?' in imgurFilename:
                        # The regex doesn't catch a "?" at the end of the filename, so we remove it here.
                        imgurFilename = imgurFilename[:imgurFilename.find('?')]

                    self.checkHigherRes(submission.url)

                elif 'http://imgur.com/' in submission.url and 'http://imgur.com/' not in submission.url:
                    # This is an Imgur page with a single image.
                    htmlSource = requests.get(submission.url).text # download the image's page
                    soup = BeautifulSoup(htmlSource)
                    try:
                        imageUrl = soup.select('.image div img')[0]['src']
                        if imageUrl.startswith('//'):
                            # if no schema is supplied in the url, prepend 'http:' to it
                            imageUrl = 'http:' + imageUrl
                        imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

                        if '?' in imageUrl:
                            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
                        else:
                            imageFile = imageUrl[imageUrl.rfind('/') + 1:]

                        self.checkHigherRes(imageUrl)
                    except Exception as e:
                        print e.message

            time.sleep(1800)

def main():
    bot = RedditBot('usernname', 'passsword') # Change 'user' and 'pass' to your login info
    try:
        bot.start()
    except:
        raise

    return 0

if __name__ == '__main__':
    main()