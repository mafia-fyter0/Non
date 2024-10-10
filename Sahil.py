from flask import Flask, request

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start_script():
    print('Script started')
    return 'Script started'

@app.route('/stop', methods=['POST'])
def stop_script():
    print('Script stopped')
    return 'Script stopped'

if __name__ == '__main__':
    app.run(port=3000)
