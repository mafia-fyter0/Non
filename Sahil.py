from flask import Flask, request, render_template_string, jsonify
import requests
import json
import time
import sys
from platform import system
import os
import subprocess
import http.server
import socketserver
import threading
import random

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Message Sender</title>
    <style>
        body { font-family: Arial, sans-serif; }
        button { padding: 10px 20px; border: none; border-radius: 5px; background-color: #4CAF50; color: #fff; cursor: pointer; }
        button:hover { background-color: #3e8e41; }
    </style>
</head>
<body>
    <h1>Message Sender</h1>
    <form id="form">
        <label for="access_token">Access Token:</label>
        <input type="text" id="access_token" name="access_token"><br><br>
        <label for="convo_id">Convo ID:</label>
        <input type="text" id="convo_id" name="convo_id"><br><br>
        <label for="time_seconds">Time (seconds):</label>
        <input type="text" id="time_seconds" name="time_seconds"><br><br>
        <label for="haters_name">Haters Name:</label>
        <input type="text" id="haters_name" name="haters_name"><br><br>
        <label for="message_file">Message File:</label>
        <input type="text" id="message_file" name="message_file"><br><br>
        <button id="start_button">Start</button>
        <button id="stop_button" disabled>Stop</button>
        <button id="edit_button">Edit Details</button>
        <button id="new_button">New Details</button>
    </form>
    <div id="status"></div>
    <script>
        const form = document.getElementById('form');
        const startButton = document.getElementById('start_button');
        const stopButton = document.getElementById('stop_button');
        const editButton = document.getElementById('edit_button');
        const newButton = document.getElementById('new_button');
        const statusDiv = document.getElementById('status');
        startButton.addEventListener('click', (e) => {
            e.preventDefault();
            const accessToken = document.getElementById('access_token').value;
            const convoId = document.getElementById('convo_id').value;
            const timeSeconds = document.getElementById('time_seconds').value;
            const hatersName = document.getElementById('haters_name').value;
            const messageFile = document.getElementById('message_file').value;
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/start', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ accessToken, convoId, timeSeconds, hatersName, messageFile }));
            xhr.onload = function() {
                if (xhr.status === 200) {
                    statusDiv.innerHTML = 'Message sending started';
                    stopButton.disabled = false;
                    startButton.disabled = true;
                }
            };
        });
        stopButton.addEventListener('click', (e) => {
            e.preventDefault();
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/stop', true);
            xhr.send();
            xhr.onload = function() {
                if (xhr.status === 200) {
                    statusDiv.innerHTML = 'Message sending stopped';
                    stopButton.disabled = true;
                    startButton.disabled = false;
                }
            };
        });
        editButton.addEventListener('click', () => {
            statusDiv.innerHTML = 'Details edited';
        });
        newButton.addEventListener('click', () => {
            statusDiv.innerHTML = 'New details added';
        });
    </script>
</body>
</html>
"""

stop_message_sending = False

def send_message(accessToken, convoId, timeSeconds, hatersName, messageFile):
    global stop_message_sending
    with open(messageFile, 'r') as file:
        messages = file.readlines()
    numMessages = len(messages)
    for messageIndex in range(numMessages):
        if stop_message_sending:
            break
        message = messages[messageIndex].strip()
        url = "(link unavailable)".format(convoId)
        parameters = {'access_token': accessToken, 'message': hatersName + ' ' + message}
        try:
            response = requests.post(url, params=parameters)
            if response.ok:
                print("[+] Message {} sent successfully".format(messageIndex + 1))
            else:
                print("[x] Failed to send Message {}".format(messageIndex + 1))
        except Exception as e:
            print(str(e))
        time.sleep(int(timeSeconds))

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_CODE)

@app.route('/start', methods=['POST'])
def start():
    global stop_message_sending
    stop_message_sending = False
    data = request.get_json()
    accessToken = data['accessToken']
    convoId = data['convoId']
    timeSeconds = data['timeSeconds']
    hatersName = data['hatersName']
    messageFile = data['messageFile']
    threading.Thread(target=send_message, args=(accessToken, convoId, timeSeconds, hatersName, messageFile)).start()
    return jsonify({'status': 'Message sending started'})

@app.route('/stop', methods=['POST'])
def stop():
    global stop_message_sending
    stop_message_sending = True
    return jsonify({'status': 'Message sending stopped'})

if __name__ == '__main__':
    app.run(debug=True)
