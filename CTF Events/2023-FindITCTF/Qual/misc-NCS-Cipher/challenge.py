import os
import random
import subprocess
import requests
from yt_dlp import YoutubeDL

resources = requests.get("https://raw.githubusercontent.com/dundorma/TinDog-WebDev-Bootcamp/master/random-data/NoCopyrightSounds.json").json()
flag = "FindITCTF{REDACTED}"
flag = flag[10:-1]

def get_resource(val):
    return random.choice([i for i in resources if i["seqId"] == val])["id"]["videoId"]

def download(val):
    resource = get_resource(val)
    ydl_opts = { 
        "format": 'bestaudio',
        'extractaudio' : True,
        'audioformat': "mp3",
        "outtmpl": '%(id)s' + '.mp3'}
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v='+resource])
    
    return(resource)

tracks = [download(ord(i)) for i in flag]

inputs = sum([["-i", f"{i}.mp3"] for i in tracks], [])
filters = "".join(f"[{i}:a]atrim=end=5,asetpts=PTS-STARTPTS[a{i}];" for i in range(len(tracks))) + \
          "".join(f"[a{i}]" for i in range(len(tracks))) + \
          f"concat=n={len(tracks)}:v=0:a=1[a]"

subprocess.run(["ffmpeg"] + inputs + ["-filter_complex", filters, "-map", "[a]", "flag.mp3"])