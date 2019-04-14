from flask import Flask
import importlib

app = Flask(__name__)

# load routes
importlib.import_module('Nymph.routes')
