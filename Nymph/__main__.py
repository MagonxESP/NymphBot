from Nymph import app, nymph_discord
from threading import Thread


# init threads
flask_runtime = Thread(target=app.run, args=('0.0.0.0', 5000))
flask_runtime.start()

# run discord bot in main thread
nymph_discord.run()
