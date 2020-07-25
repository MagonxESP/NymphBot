import Nymph.settings as settings
import twitter
import hashlib
import datetime
from discord.ext import commands
import asyncio
from Nymph.storage import SelectedTextChannel, Tweet
from pony.orm import db_session, select, desc


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
            self.saveStatus(posted_status)
        except twitter.error.TwitterError:
            try:
                tweet = self.getLastTweet(status)

                if tweet is not None:
                    api.PostRetweet(int(tweet.tweet_id))
            except twitter.error.TwitterError:
                _hash = hashlib.md5(str(datetime.datetime.now().timestamp()).encode())
                new_status = status + ' #' + _hash.hexdigest()[:5]
                posted_status = api.PostUpdate(new_status)
                posted_status.text = status  # prevents save tweet with new status
                self.saveStatus(posted_status)

    @db_session
    def saveStatus(self, tweet):
        tweet_dict = tweet.AsDict()
        Tweet(
            status=tweet_dict['text'],
            tweet_id=str(tweet_dict['id']),
            create_time=int(datetime.datetime.now().timestamp())
        )

    def getLastTweet(self, status):
        tweet = select(tweet for tweet in Tweet if status == tweet.status)\
            .order_by(desc(Tweet.create_time))\
            .first()

        return tweet

    def createdTimeToTimestamp(self, created_at):
        date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        return date.timestamp()


class NymphDiscord(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='!')
        self.add_command(commands.Command(self.status))

    def run(self):
        super().run(settings.DISCORD_TOKEN)

    def post(self, status, options=None):
        channels = select(channel for channel in SelectedTextChannel)

        for c in channels:
            channel = self.get_channel(int(c.channel_id))
            asyncio.run_coroutine_threadsafe(channel.send(status), self.loop)

    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        channel_id = ctx.message.channel.id
        channels = select(channel for channel in SelectedTextChannel if channel.channel_id == str(channel_id))

        if len(channels) == 0:
            with db_session:
                SelectedTextChannel(channel_id=str(channel_id))

            await ctx.send('Aqui subire el estado del server OwO')
        else:
            await ctx.send('Ya estoy usando este canal')
