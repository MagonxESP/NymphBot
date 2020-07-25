from Nymph import app, nymph_discord
from Nymph.storage import db
import os

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
database_directory = os.path.join(root, 'data')

if os.path.exists(database_directory) is False:
    os.makedirs(database_directory, exist_ok=True)

db.bind(provider='sqlite', filename=os.path.join(database_directory, 'storage.sqlite'), create_db=True)
db.generate_mapping(create_tables=True)

nymph_discord.loop.create_task(app.run_task('0.0.0.0', 5000, debug=True))
nymph_discord.run()
