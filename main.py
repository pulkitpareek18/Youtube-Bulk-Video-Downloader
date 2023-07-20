from flask import Flask, request, render_template
import pandas
import validators
import os
import json
from werkzeug.utils import secure_filename
import shortuuid
import threading
import time
from pytube import YouTube

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = "static/uploads"


def cleanGarbage():
    threading.Timer(600, cleanGarbage).start()
    for file in os.listdir(UPLOAD_FOLDER):
        if file != ".gitkeep":
            os.remove(os.path.join(UPLOAD_FOLDER, file))
    print(f'Garbage Cleaned at {time.strftime("%m/%d/%Y, %H:%M:%S")}.')


cleanGarbage()


def getYtVideoDownloadUrl(ytUrl):
    try:
        yt = YouTube(ytUrl)
        streams = yt.streams
        stream = streams.filter(progressive=True, type="video", file_extension="mp4")
        stream = stream.order_by("resolution").desc().first()
        return stream.url
    except:
        print(f"Can't download {ytUrl}")


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {"error": "No File Part."}

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {"error": "No File Selected."}

        if not allowed_file(file.filename):
            return {"error": "Please enter a CSV File."}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = ".".join(filename.split(".")[:-1]) + "_" + shortuuid.uuid() + "." + filename.split(".")[-1]
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            # reading the CSV file
            csvFile = pandas.read_csv(os.path.join(UPLOAD_FOLDER, filename))
            csvFileList = csvFile.values.tolist()

            # displaying the contents of the CSV file
            urlList = list()
            for data in csvFileList:
                if validators.url(str(data[0])):
                    urlList.append(getYtVideoDownloadUrl(data[0]))


            return json.dumps({"success": urlList})
    else:
        return {"error": "Please make a valid Request."}


@app.route("/")
def home():
    return render_template("index.html")


# No match found for pattern: var for={(.*?)}; is from pytube module, not the fault of this app.
# This app uses pytube from the GitHub repository https://github.com/pulkitpareek18/pytube

app.run(debug=True)
