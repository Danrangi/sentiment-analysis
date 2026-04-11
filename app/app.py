from flask import Flask, render_template, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import predict

app = Flask(__name__)

# ── UI route ──────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# ── Form submission route (returns result page) ───────────────────────────────
@app.route('/analyse', methods=['POST'])
def analyse():
    text   = request.form.get('feedback', '').strip()
    result = predict(text)
    return render_template('result.html', result=result)

# ── JSON API endpoint (for programmatic use) ──────────────────────────────────
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data   = request.get_json(force=True)
    text   = data.get('text', '')
    result = predict(text)
    return jsonify(result)

# ── Health check ──────────────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'SVM + TF-IDF (CondB_Unigram)'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
