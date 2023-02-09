#Under t.me/feelded copyright.

import os
class Config(object):
    APP_ID = int(os.environ.get("APP_ID", 666))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") #Without @
    OWNER_ID = int(os.environ.get("OWNER_ID", 9876543210))
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
    GENIUS_API_KEY = os.environ.get("GENIUS_API_KEY", "")
