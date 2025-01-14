# notes
'''
This file is for creating a Flask server to be used for the dash app.
I also initiate the cache file here.
'''
# package imports
import os
from flask_caching import Cache
from server import server

# Configure FileSystemCache
CACHE_DIR = os.path.join(os.getcwd(), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)  # make if didn't exist
CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': CACHE_DIR,
}
cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)

