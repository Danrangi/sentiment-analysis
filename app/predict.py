import re
import joblib
import nltk
import os

nltk.download('stopwords', quiet=True)
nltk.download('punkt',     quiet=True)
nltk.download('punkt_tab', quiet=True)

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('english'))

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.pkl')
VEC_PATH   = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')
LE_PATH    = os.path.join(BASE_DIR, 'models', 'label_encoder.pkl')

# ── Load artefacts once at import time ────────────────────────────────────────
model   = joblib.load(MODEL_PATH)
vec     = joblib.load(VEC_PATH)
le      = joblib.load(LE_PATH)

# ── Preprocessing (must match CondB used during training) ────────────────────
def preprocess(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+',           '', text)
    text = re.sub(r'#',              '', text)
    text = re.sub(r'&amp;',         'and', text)
    text = re.sub(r'[^a-z\s]',      '', text)
    text = re.sub(r'\s+',           ' ', text).strip()
    return text

# ── Sentiment metadata ────────────────────────────────────────────────────────
SENTIMENT_META = {
    'negative': {
        'emoji':       '😠',
        'color':       '#E63946',
        'bg':          '#fff0f0',
        'border':      '#E63946',
        'description': 'The feedback expresses dissatisfaction, frustration, or a complaint.',
        'advice':      'Immediate attention recommended. Consider reaching out to the customer.'
    },
    'neutral': {
        'emoji':       '😐',
        'color':       '#457B9D',
        'bg':          '#f0f6fb',
        'border':      '#457B9D',
        'description': 'The feedback is factual or informational with no strong sentiment.',
        'advice':      'Monitor for follow-up. May indicate an unresolved question.'
    },
    'positive': {
        'emoji':       '😊',
        'color':       '#2DC653',
        'bg':          '#f0fbf3',
        'border':      '#2DC653',
        'description': 'The feedback expresses satisfaction, praise, or appreciation.',
        'advice':      'Great outcome! Consider using as a testimonial or staff recognition.'
    }
}

def predict(text: str) -> dict:
    """
    Takes raw input text, preprocesses it, runs the model,
    and returns a structured result dictionary.
    """
    if not text or not text.strip():
        return {'error': 'No text provided.'}

    cleaned   = preprocess(text)
    X         = vec.transform([cleaned])
    y_encoded = model.predict(X)[0]
    label     = le.inverse_transform([y_encoded])[0]
    meta      = SENTIMENT_META[label]

    # Confidence proxy: decision function distance from boundary (SVM)
    try:
        scores     = model.decision_function(X)[0]
        confidence = round(float(max(scores) - min(scores)) / (max(scores) - min(scores) + 1e-9) * 100, 1)
        confidence = min(max(confidence, 55.0), 99.0)   # clamp to realistic range
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
