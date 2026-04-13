import sys
import os
import time
import threading
import webbrowser

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from flask import Flask, render_template, request, jsonify
from predict import predict

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates'),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static')
)

last_heartbeat = time.time()
HEARTBEAT_TIMEOUT = 8

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    text   = request.form.get('feedback', '').strip()
    result = predict(text)
    return render_template('result.html', result=result)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data   = request.get_json(force=True)
    result = predict(data.get('text', ''))
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    global last_heartbeat
    last_heartbeat = time.time()
    return jsonify({'alive': True})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    threading.Thread(target=_delayed_shutdown).start()
    return jsonify({'status': 'shutting down'})

def _delayed_shutdown():
    time.sleep(1)
    os._exit(0)

def watch_heartbeat():
    global last_heartbeat
    time.sleep(15)
    while True:
        time.sleep(3)
        if time.time() - last_heartbeat > HEARTBEAT_TIMEOUT:
            os._exit(0)

def open_browser():
    time.sleep(1.8)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    threading.Thread(target=watch_heartbeat, daemon=True).start()
    threading.Thread(target=open_browser,    daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
