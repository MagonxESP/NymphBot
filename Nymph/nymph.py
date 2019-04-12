import Nymph.settings as settings
import twitter
import json
import os
import time
import datetime


class Nymph:

    def __init__(self):
        self.__apis = [
            NymphTwitter()
        ]

    def post(self, status, options=None):
        for api in self.__apis:
            api.post(status, options)


class ApiService:

    def post(self, status, options=None):
        raise NotImplemented


class NymphTwitter(ApiService):

    def __init__(self):
        self.__api = twitter.Api(
            consumer_key=settings.CONSUMER_API_KEY,
            consumer_secret=settings.CONSUMER_API_KEY_SECRET,
            access_token_key=settings.ACCESS_TOKEN,
            access_token_secret=settings.ACCESS_TOKEN_SECRET
        )

    def post(self, status, options=None):
        try:
            api = self.__api
            posted_status = api.PostUpdate(status)
            self.saveStatus(posted_status.AsDict())
        except twitter.error.TwitterError as e:
            pass

    def saveStatus(self, status):
        try:
            tweets = []

            if os.path.isfile('tweets.json'):
                file = open('tweets.json', 'r')
                tweets = json.loads(file.read())
                file.close()

            tweets.append(status)
            file = open('tweets.json', 'w')
            file.write(json.dumps(tweets))
            file.close()
        except IOError as e:
            pass

    def getLastTweet(self, status):
        with open('tweets.json', 'r') as file:
            tweets = json.loads(file.read())

        tweets.sort(key=lambda item: item['created_at'])

        tweets_same_status = []
        for tweet in tweets:
            if tweet['text'] == status:
                tweets_same_status.append(tweet)

    def createdTimeToTimestamp(self, created_at):
        # timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
        # datetime.datetime.fromisoformat()
        pass


class NymphDiscord(ApiService):
    pass
