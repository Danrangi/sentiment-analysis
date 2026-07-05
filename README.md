# ✈️ SentiAir — Airline Customer Feedback Sentiment Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Accuracy](https://img.shields.io/badge/Accuracy-79.66%25-brightgreen.svg)]()

> Intelligent sentiment analysis for airline customer feedback on Twitter. Powered by machine learning to understand customer satisfaction at scale.

---

## 📋 Overview

**SentiAir** is a machine learning-powered web application that automatically classifies airline customer feedback into three sentiment categories:

- 😊 **Positive** — Satisfied customers and praise
- 😐 **Neutral** — Informational or balanced feedback  
- 😞 **Negative** — Complaints and concerns

Built on a **Support Vector Machine (LinearSVC)** trained with the Twitter US Airline Sentiment Dataset, this tool helps airlines monitor brand sentiment and respond to customer feedback in real-time.

---

## 🎯 Key Features

- ✅ **High Accuracy**: 79.66% classification accuracy with macro F1 score of 0.7342
- ⚡ **Fast Predictions**: Real-time sentiment classification on user input
- 🌐 **Web-based Interface**: Easy-to-use UI for analyzing individual tweets or feedback
- 📊 **Reliable Model**: Trained on thousands of real airline customer tweets
- 🔧 **TF-IDF Features**: Unigram-based feature extraction for robust text analysis

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **Accuracy** | 79.66% |
| **Macro F1-Score** | 0.7342 |
| **Algorithm** | Linear SVC |
| **Features** | TF-IDF Unigram |
| **Dataset Size** | Twitter US Airline Sentiment |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Danrangi/sentiment-analysis.git
   cd sentiment-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   - Open your browser and navigate to `http://localhost:5000`

---

## 📁 Project Structure

```
sentiment-analysis/
├── README.md                 # Project documentation
├── app.py                    # Flask web application
├── requirements.txt          # Python dependencies
├── model/
│   ├── sentiment_model.pkl   # Trained ML model
│   └── tfidf_vectorizer.pkl  # TF-IDF vectorizer
├── data/
│   ├── raw/                  # Raw dataset
│   └── processed/            # Processed data
├── notebooks/
│   └── analysis.ipynb        # Exploratory data analysis
└── static/
    ├── css/
    ├── js/
    └── templates/            # HTML templates
```

---

## 💡 How It Works

1. **Input**: User submits airline feedback or a tweet
2. **Preprocessing**: Text is cleaned and normalized
3. **Vectorization**: TF-IDF converts text into numerical features
4. **Classification**: Linear SVC model predicts sentiment
5. **Output**: Application displays prediction with confidence score

```
[User Input] → [Text Preprocessing] → [TF-IDF Vectorization] → [ML Model] → [Sentiment Prediction]
```

---

## 🛠️ Technologies Used

- **Machine Learning**: scikit-learn (LinearSVC, TfidfVectorizer)
- **Web Framework**: Flask
- **Data Processing**: pandas, NumPy
- **NLP**: NLTK, scikit-learn
- **Frontend**: HTML, CSS, JavaScript

---

## 📚 Dataset

The model is trained on the **Twitter US Airline Sentiment Dataset**, containing:
- 14,640 labeled tweets
- Real airline customer feedback
- Balanced classes across three sentiment categories

**Source**: [Kaggle - Twitter US Airline Sentiment](https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment)

---

## 🔍 Example Usage

```python
from model import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.predict("Great flight experience, highly recommend!")
# Output: {'sentiment': 'positive', 'confidence': 0.85}
```

---

## 📈 Performance Insights

The model performs well across all sentiment categories:
- **Positive Class**: Accurately identifies satisfied customer feedback
- **Negative Class**: Effectively catches complaints and concerns
- **Neutral Class**: Distinguishes informational posts from opinions

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact & Support

Have questions or feedback? Feel free to reach out:

- **GitHub Issues**: [Report a bug](https://github.com/Danrangi/sentiment-analysis/issues)
- **GitHub Discussions**: [Start a discussion](https://github.com/Danrangi/sentiment-analysis/discussions)

---

## 🙏 Acknowledgments

- Special thanks to CrowdFlower for the Twitter US Airline Sentiment Dataset
- scikit-learn community for excellent ML tools
- All contributors who have helped improve this project

---

**Made with ❤️ for better airline customer experience**
