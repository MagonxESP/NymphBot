from Nymph import app, nymph_discord


nymph_discord.loop.create_task(app.run_task('0.0.0.0', 5000, debug=True))
nymph_discord.run()
