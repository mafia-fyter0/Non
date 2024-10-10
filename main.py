from flask import Flask, render_template, request
import requests
import json
import time
import threading
import schedule

app = Flask(__name__)

conv_id = ""
haters_name = ""
token = ""
time_seconds = ""
file_path = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global conv_id, haters_name, token, time_seconds, file_path
    conv_id = request.form["conv_id"]
    haters_name = request.form["haters_name"]
    token = request.form["token"]
    time_seconds = request.form["time_seconds"]
    file_path = request.form["file_path"]

    thread = threading.Thread(target=run_script)
    thread.daemon = True  
    thread.start()

    return "Script started successfully!"

@app.route("/stop", methods=["POST"])
def stop():
    # Script ko stop karne ka logic yahaan likhein
    return "Script stopped successfully!"

def run_script():
    while True:
        # Script ko run karne ka logic yahaan likhein
        time.sleep(int(time_seconds))

def start_script():
    thread = threading.Thread(target=run_script)
    thread.daemon = True  
    thread.start()

schedule.every().day.at("00:00").do(start_script)  

if __name__ == "__main__":
    app.run(port=5000)
