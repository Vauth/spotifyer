#Under t.me/feelded copyright.

import re
import urllib
import spotipy
import lyricsgenius
from config import Config
from html_telegraph_poster import TelegraphPoster
from spotipy.oauth2 import SpotifyClientCredentials

#Vars
CI = Config.SPOTIFY_CLIENT_ID
CS = Config.SPOTIFY_CLIENT_SECRET
SCM = SpotifyClientCredentials(client_id=CI, client_secret=CS)
GENIUS = Config.GENIUS_API_KEY
USERNAME = Config.BOT_USERNAME

#Clients
sp = spotipy.Spotify(client_credentials_manager=SCM)
genius = lyricsgenius.Genius(GENIUS)

#Spotify Search
def sp_search(query):
    z = sp.search(str(query), limit=2)
    url = z["tracks"]["items"][0]["external_urls"]["spotify"]
    return url

#Spotify track data
def track_data(url):
    id = (url.split("/"))[4]
    runurl = f"spotify:track:{id}"
    track = sp.track(runurl)
    track_name = track["name"]
    track_artist = track["artists"][0]["name"]
    track_image = track["album"]["images"][0]["url"]
    return {"name":track_name, "artist":track_artist, "image":track_image}

#Youtube search
def yt_search(texts):
    try:
        texts = urllib.parse.quote(texts)
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={texts}")

        user_data = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_link = []
        k = 0
        for i in user_data:
            if user_data:
                video_link.append("https://www.youtube.com/watch?v=" + user_data[k])
            k += 1
            if k > 3:
                break
        if video_link:
            return video_link[0]
        return "Couldnt fetch results"
    except Exception:
        return "Couldnt fetch results"

#Telegraph poster
def post_to_telegraph(page_title, html_format_content):
    post_client = TelegraphPoster(use_api=True)
    auth_name = (USERNAME)[:-3]
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=page_title,
        author=auth_name,
        author_url=f"https://t.me/{USERNAME}",
        text=html_format_content,
    )
    return post_page["url"]

#Lyrics generator
def lyrics_gen(songname):
    "Telegraph lyrics"
    try:
        g = genius.search_song(songname)
        ly = g.lyrics
        text = ly.replace(f"{g.title} Lyrics", "").replace("Embed", "")
        name = f"{g.title} - {g.artist}"
    except Exception as e:
        return str(e)
    try:
        img = g.song_art_image_url
    except Exception:
        img = "https://telegra.ph/file/e8729169fceb858b075d2.jpg"
            
    telegraph = f"""
    <p align="center"><a href="#"><img src="{img}" width="250"></a></p>
    <p><pre>{text}</pre></p>
    """
    link = post_to_telegraph(name , telegraph)
    thislink = link
    return thislink

#Readable time
def readable_time(seconds: int) -> str:
    count = 0
    uptime = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    tlen = len(time_list)
    for x in range(tlen):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        uptime += time_list.pop() + ":"
    time_list.reverse()
    uptime += ":".join(time_list)
    return uptime

#Emoji lang
def emolang(text, reverse=False): #UnicoderBot to get range
	char = [str(chr(i)) for i in range(33, 130)]
	emo = [str(chr(i)) for i in range(128136, 128136+int(len(char)))]
	
	odict = {char[i]:emo[i] for i in range(0, int(len(char)))}
	rdict = {v: k for k, v in odict.items()}
	
	tr = text.translate(text.maketrans(odict))
	rv = tr.translate(tr.maketrans(rdict))
	
	if reverse == True:
		return str(rv)
	else:
		return str(tr)
