from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Script Runner</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: #fff;
            cursor: pointer;
        }
        button:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <h1>Script Runner</h1>
    <form id="form">
        <label for="conv_id">Conv ID:</label>
        <input type="text" id="conv_id" name="conv_id"><br><br>
        <label for="haters_name">Haters Name:</label>
        <input type="text" id="haters_name" name="haters_name"><br><br>
        <label for="token">Token:</label>
        <input type="text" id="token" name="token"><br><br>
        <label for="time_seconds">Time (seconds):</label>
        <input type="text" id="time_seconds" name="time_seconds"><br><br>
        <label for="file_path">File:</label>
        <input type="text" id="file_path" name="file_path"><br><br>
        <button id="start_button">Start Script</button>
        <button id="stop_button" disabled>Stop Script</button>
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
            const convId = document.getElementById('conv_id').value;
            const hatersName = document.getElementById('haters_name').value;
            const token = document.getElementById('token').value;
            const timeSeconds = document.getElementById('time_seconds').value;
            const filePath = document.getElementById('file_path').value;
            
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/start', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ convId, hatersName, token, timeSeconds, filePath }));
            
            xhr.onload = function() {
                if (xhr.status === 200) {
                    statusDiv.innerHTML = 'Script started';
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
                    statusDiv.innerHTML = 'Script stopped';
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

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_CODE)

@app.route('/start', methods=['POST'])
def start_script():
    data = request.get_json()
    print('Script started with data:', data)
    return 'Script started'

@app.route('/stop', methods=['POST'])
def stop_script():
    print('Script stopped')
    return 'Script stopped'

if __name__ == '__main__':
    app.run(port=3000)
