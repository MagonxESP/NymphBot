from dotenv import load_dotenv
from os.path import join, dirname
import os

# load .env file
env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
CONSUMER_API_KEY = os.getenv('CONSUMER_API_KEY')
CONSUMER_API_KEY_SECRET = os.getenv('CONSUMER_API_KEY_SECRET')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
