import Nymph.settings as settings
import twitter
import json
import os
import hashlib
import datetime
from discord.ext import commands
import asyncio
from Nymph.storage import Storage


class Nymph:

    __routes = []

    def __init__(self):
        pass

    def addRouteCallback(self, route, callback):
        self.__routes.append({
            'name': route,
            'callback': callback
        })

    def post(self, status, options=None):
        for route in self.__routes:
            if route['name'] == 'post':
                route['callback'](status, options)


class NymphTwitter:

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
                _hash = hashlib.md5(str(datetime.datetime.now().timestamp()).encode())
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


class NymphDiscord(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!')
        self.add_command(commands.Command(self.status))
        self._storage = Storage('discord')
        self._status_channels = self._storage.get('status_channels')

        if self._status_channels is None:
            self._status_channels = []

    def run(self):
        super().run(settings.DISCORD_TOKEN)

    def post(self, status, options=None):
        for channel_id in self._status_channels:
            channel = self.get_channel(channel_id)
            asyncio.run_coroutine_threadsafe(channel.send(status), self.loop)

    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        channel_id = ctx.message.channel.id

        if self._status_channels.count(channel_id) > 0:
            self._status_channels.append(channel_id)
            self._storage.set('status_channels', self._status_channels)
            await ctx.send('Aqui subire el estado del server OwO')
        else:
            await ctx.send('Ya estoy usando este canal')
