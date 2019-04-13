import Nymph.settings as settings
import twitter
import json
import os
import hashlib
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
        api = self.__api

        try:
            posted_status = api.PostUpdate(status)
            self.saveStatus(posted_status.AsDict())
        except twitter.error.TwitterError:
            try:
                tweet = self.getLastTweet(status)
                api.PostRetweet(tweet['id'])
            except twitter.error.TwitterError:
                _hash = hashlib.md5()
                new_status = status + ' #' + _hash.hexdigest()[:5]
                posted_status = api.PostUpdate(new_status)
                posted_status.text = status  # prevents save tweet with new status
                self.saveStatus(posted_status.AsDict())

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
        file = open('tweets.json', 'r')
        tweets = json.loads(file.read())

        tweets = sorted(tweets, key=lambda item: self.createdTimeToTimestamp(item['created_at']))

        tweets_same_status = []
        for tweet in tweets:
            if tweet['text'] == status:
                tweets_same_status.append(tweet)

        return tweets_same_status[0]

    def createdTimeToTimestamp(self, created_at):
        date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        return date.timestamp()


class NymphDiscord(ApiService):
    pass
