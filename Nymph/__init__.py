from flask import Flask
from threading import Thread
import Nymph.nymph
import importlib


app = Flask(__name__)

# main bot instance
nymph_bot = Nymph.nymph.Nymph()

# social bot instances
nymph_twitter = Nymph.nymph.NymphTwitter()
nymph_discord = Nymph.nymph.NymphDiscord()

# add flask route callbacks to main bot instance
nymph_bot.addRouteCallback('post', nymph_twitter.post)
nymph_bot.addRouteCallback('post', nymph_discord.post)

# load routes
importlib.import_module('Nymph.routes')

# init threads
discord_bot_runtime = Thread(target=nymph_discord.run)
discord_bot_runtime.run()
