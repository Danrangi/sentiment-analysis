import sys
import os
import re
import time
import threading
import webbrowser
import joblib
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt',     quiet=True)
nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords
from flask import Flask, render_template, request, jsonify

# ── Resolve paths correctly inside frozen .exe ────────────────
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'app', 'templates')
STATIC_DIR   = os.path.join(BASE_DIR, 'app', 'static')
MODEL_PATH   = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
VEC_PATH     = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')
LE_PATH      = os.path.join(BASE_DIR, 'models', 'label_encoder.pkl')

# ── Load model artefacts ──────────────────────────────────────
model = joblib.load(MODEL_PATH)
vec   = joblib.load(VEC_PATH)
le    = joblib.load(LE_PATH)

# ── Preprocessing (Condition B — minimal) ────────────────────
def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+',           '', text)
    text = re.sub(r'#',              '', text)
    text = re.sub(r'&amp;',         'and', text)
    text = re.sub(r'[^a-z\s]',      '', text)
    text = re.sub(r'\s+',           ' ', text).strip()
    return text

# ── Sentiment metadata ────────────────────────────────────────
SENTIMENT_META = {
    'negative': {
        'emoji': '😠', 'color': '#E63946', 'bg': '#fff0f0', 'border': '#E63946',
        'description': 'The feedback expresses dissatisfaction, frustration, or a complaint.',
        'advice': 'Immediate attention recommended. Consider reaching out to the customer.'
    },
    'neutral': {
        'emoji': '😐', 'color': '#457B9D', 'bg': '#f0f6fb', 'border': '#457B9D',
        'description': 'The feedback is factual or informational with no strong sentiment.',
        'advice': 'Monitor for follow-up. May indicate an unresolved question.'
    },
    'positive': {
        'emoji': '😊', 'color': '#2DC653', 'bg': '#f0fbf3', 'border': '#2DC653',
        'description': 'The feedback expresses satisfaction, praise, or appreciation.',
        'advice': 'Great outcome! Consider using as a testimonial or staff recognition.'
    }
}

def predict(text):
    if not text or not text.strip():
        return {'error': 'No text provided.'}
    cleaned   = preprocess(text)
    X         = vec.transform([cleaned])
    y_encoded = model.predict(X)[0]
    label     = le.inverse_transform([y_encoded])[0]
    meta      = SENTIMENT_META[label]
    try:
        scores     = model.decision_function(X)[0]
        confidence = round(float(max(scores) - min(scores)) / (max(scores) - min(scores) + 1e-9) * 100, 1)
        confidence = min(max(confidence, 55.0), 99.0)
    except Exception:
        confidence = None
    return {
        'label':       label,
        'emoji':       meta['emoji'],
        'color':       meta['color'],
        'bg':          meta['bg'],
        'border':      meta['border'],
        'description': meta['description'],
        'advice':      meta['advice'],
        'confidence':  confidence,
        'input_text':  text,
        'cleaned':     cleaned,
    }

# ── Flask app ─────────────────────────────────────────────────
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

last_heartbeat = time.time()

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
    threading.Thread(target=lambda: (time.sleep(1), os._exit(0))).start()
    return jsonify({'status': 'shutting down'})

# ── Heartbeat watcher ─────────────────────────────────────────
def watch_heartbeat():
    global last_heartbeat
    time.sleep(15)
    while True:
        time.sleep(3)
        if time.time() - last_heartbeat > 8:
            os._exit(0)

# ── Open browser ──────────────────────────────────────────────
def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    threading.Thread(target=watch_heartbeat, daemon=True).start()
    threading.Thread(target=open_browser,    daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
