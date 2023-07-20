from flask import Flask, request, render_template
import os
import json
import threading
import time
from pytube import YouTube
import re
import concurrent.futures

app = Flask(__name__)

def extract_youtube_urls(text):
    # Regular expression pattern to match YouTube URLs
    pattern = r"(?P<url>https?://(?:www\.|m\.)?youtube\.com/(?:watch\?v=|shorts/|embed/|v/|e/|watch\?.+&v=|youtu\.be/)(?P<id>[a-zA-Z0-9_-]+))"
    
    # Find all occurrences of the pattern in the text
    matches = re.finditer(pattern, text)
    
    # Extract and return the URLs as a list
    return [match.group("url") for match in matches]


def getYtVideoDownloadUrl(ytUrl):
    try:
        yt = YouTube(ytUrl)
        streams = yt.streams
        stream = streams.filter(progressive=True, type="video", file_extension="mp4")
        stream = stream.order_by("resolution").desc().first()
        return stream.url
    except:
        print(f"Can't download {ytUrl}")
        

@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == 'POST':
        
        if request.form['urls']:
            YtUrlList = extract_youtube_urls(request.form['urls'])
            urlList = list()
            if len(YtUrlList) != 0:
                
                    for url in YtUrlList:
                        urlList.append(url)
                        
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = executor.map(getYtVideoDownloadUrl, urlList)
                        urlList = list(results)        
                        
            else:
                
                return json.dumps({"error":"Please Enter a valid Url."})  
                
            return json.dumps({"success": urlList})
            
    else:
        
        return json.dumps({"error": "Please make a valid Request."})
    
    return json.dumps({"error": "Please Enter a Url."})

@app.route("/")
def home():
    return render_template("index.html")


# No match found for pattern: var for={(.*?)}; is from pytube module, not the fault of this app.
# This app uses pytube from the GitHub repository https://github.com/pulkitpareek18/pytube

app.run()
