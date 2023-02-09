#Under t.me/feelded copyright.

import os
import time
from config import Config
from telethon import events
from telethon import Button
from yt_dlp import YoutubeDL
from datetime import datetime
from urlextract import URLExtract
from telethon.sync import TelegramClient
from telethon.tl.types import InputWebDocument
from telethon.tl.types import DocumentAttributeAudio
from helper import track_data, yt_search, sp_search, lyrics_gen, sp, readable_time, emolang

#START TIME
StartTime = time.time()

#URLEX
extractor = URLExtract()

#CLIENT
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
BOT_TOKEN = Config.BOT_TOKEN
BOT_USERNAME = Config.BOT_USERNAME
OWNER_ID = Config.OWNER_ID
bot = TelegramClient('Spotifyer', APP_ID,  API_HASH).start(bot_token=BOT_TOKEN)

"""
INLINE
"""
@bot.on(events.InlineQuery())
async def spotify(event):
    "Spotify Search"
    #Event objects
    query_user_id = event.query.user_id
    text = event.text.replace("%20", "").replace("-", " ").replace(" - ", " ")
    
    #Text & Mode
    if text.lower().startswith("en:"):
        spl = text.lower().split("en:")
        query = str(spl[1])
        mode = "EN"
    else:
        query = text
        mode = "ORG"
    
    #Return when ''
    if text == "":
        return await event.answer([])
    
    #Run
    if query:
        try:
            res = []
            r = sp.search(q=f"{query}", limit=31)
            all = int(len(r["tracks"]["items"]) - 1)
            for i in range(0, all):
                title = r["tracks"]["items"][i]["name"]
                artist = r["tracks"]["items"][i]["artists"][0]["name"]
                album = r["tracks"]["items"][i]["album"]["name"]
                thumb = r["tracks"]["items"][i]["album"]["images"][2]["url"]
                track_url = r["tracks"]["items"][i]["external_urls"]["spotify"]
                album_url = r["tracks"]["items"][i]["album"]["external_urls"]["spotify"]
                artist_url = r["tracks"]["items"][i]["artists"][0]["external_urls"]["spotify"]
                
                if mode == "EN":
                    text = f"⁪{emolang((track_url.split('/'))[4])}"
                else:
                    text = f"**- Song:** [{title}]({track_url})\n**- Artist:** [{artist}]({artist_url})\n**- Album:** [{album}]({album_url})"
                bs = Button.switch_inline("🔍 Search Again", "", same_peer=True)
                c = event.builder.article(title=title, text=text, buttons=bs, description=f"Artist: {artist}\nAlbum: {album}", thumb=InputWebDocument(url=thumb, size=0, mime_type="image/jpeg", attributes=[]))
                res.append(c)
            await event.answer(res)
        except Exception as e:
            pass
    else:
        await event.answer([])


""" 
CMDS
"""
#START
@bot.on(events.NewMessage(pattern=f"^/start(@{BOT_USERNAME})?([\s]+)?$"))
async def ping(event):
    name = event.sender.first_name
    username = event.sender.username or "None"
    userid = event.sender.id
    mention = f"[{name}](tg://user?id={userid})"
    hmention = f"<a href='tg://user?id={userid}'>{name}</a>"
    bs = Button.switch_inline("🔍 Search", "", same_peer=True)
    await bot.send_message(event.chat_id, f"Hi {mention} !\nI'm spotify downloader bot.", reply_to=event.id, buttons=bs)
    try:
        if userid == OWNER_ID: return
        await bot.send_message(OWNER_ID, f"#START\n<b>Name:</b> {hmention}\n<b>Username:</b> @{username}\n<b>ID:</b> <code>{userid}</code>", parse_mode="HTML")
        print(f"{name} - {userid} - started me")
    except:
        print(f"{name} - {userid} - started me")

#PING
@bot.on(events.NewMessage(pattern=f"^/ping(@{BOT_USERNAME})?([\s]+)?$"))
async def ping(event):
    start = datetime.now()
    ping = await bot.send_message(event.chat_id, "𝗣𝗼𝗻𝗴", reply_to=event.id)
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = readable_time(time.time() - StartTime)
    await ping.edit(f"𝗣𝗶𝗻𝗴: `{ms}` 𝗆𝗌\n𝗨𝗽𝘁𝗶𝗺𝗲: `{uptime}`")

#HELP
@bot.on(events.NewMessage(pattern=f"^/help(@{BOT_USERNAME})?([\s]+)?$"))
async def help(event):
    bs = Button.url("Dev", "https://t.me/feelded")
    await bot.send_message(event.chat_id, f"Just send any spotify link or search using @{BOT_USERNAME} inline mode.", buttons=bs, reply_to=event.id)

#DOWNLOAD
@bot.on(events.NewMessage())
async def spdata(event):
    try:
        if (event and event.via_bot and event.text.startswith('⁪')):
            data = track_data(f"https://open.spotify.com/track/{emolang(event.text.replace('⁪', ''), reverse=True)}")
        else:
            urls = extractor.find_urls(event.text)
            if (urls and "spotify.com/track/" in str(urls[0])):
                data = track_data(str(urls[0]))
            else:
                return
        
        title = data["name"]
        artist = data["artist"]
        yt_link = yt_search(f"{title} {artist} lyrics")
        sp_link = sp_search(f"{title} {artist}")
        lyrics = lyrics_gen(f"{title} {artist}")

        ydl_opts = {'format':'bestaudio[ext=m4a]', 'quiet':True, 'no_warnings':True}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
            
        new_audio_file = f"{title} - {artist} [{event.id}].m4a"
        os.rename(audio_file, new_audio_file)
        
        spb = Button.url("🎧 Spotify", sp_link)
        ytb = Button.url("🎬 YouTube", yt_link)
        lyb = Button.url("📝 Lyrics", lyrics)
        if lyrics.startswith("http"): bs = [[spb, ytb], [lyb]]
        else: bs = [spb, ytb]
        
        await bot.send_file(event.chat_id, new_audio_file, attributes=[DocumentAttributeAudio(title=title, performer=artist, duration=int(info_dict["duration"]))], thumb=None, buttons=bs, reply_to=event.id)
        os.remove(new_audio_file)
        
    except Exception as e:
        try:
            os.remove(audio_file)
            os.remove(new_audio_file)
        except:
            pass
        return await bot.send_message(event.chat_id, f"**ERROR:**\n`{e}`", reply_to=event.id)
#RUN
print("Bot Started.")
bot.run_until_disconnected()
