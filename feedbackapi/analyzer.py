from textblob import TextBlob
from .models import Feedback
from keybert import KeyBERT
from transformers import pipeline
import nltk
import re


nltk.download('punkt')

# Initialize models once
kw_model = KeyBERT()
aspect_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)



def extract_keywords(text):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words='english',
        top_n=3
    )
    return ', '.join([kw for kw, _ in keywords])


def detect_emotion(text):
    try:
        result = emotion_model(text)[0][0]  # top_k=1 returns list of lists
        return result['label'].capitalize()
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return "Neutral"



def split_into_clauses(text):
    # Split on punctuation and common conjunctions for finer sentiment detection
    clauses = re.split(r'[.!?;,]| but | however | although | and ', text, flags=re.IGNORECASE)
    return [clause.strip() for clause in clauses if clause.strip()]


def get_aspect_sentiments(text):
    aspects = {}
    clauses = split_into_clauses(text)

    for clause in clauses:
        result = aspect_model(clause)[0]
        label = result['label']
        score = result['score']

        if label.startswith("1") or label.startswith("2"):
            sentiment = "Negative"
        elif label.startswith("3"):
            sentiment = "Neutral"
        else:
            sentiment = "Positive"

        aspects[clause] = {
            "sentiment": sentiment,
            "confidence": round(score, 2)
        }

    return aspects


def analyze_feedback(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Aspect-level analysis
    aspect_sentiments = get_aspect_sentiments(text)
    sentiment_labels = [info['sentiment'] for info in aspect_sentiments.values()]

    # Count each sentiment type
    pos_count = sentiment_labels.count("Positive")
    neg_count = sentiment_labels.count("Negative")

    # Decision logic
    if pos_count > 0 and neg_count > 0:
        sentiment = "Mixed"
    elif pos_count > 0:
        sentiment = "Positive"
    elif neg_count > 0:
        sentiment = "Negative"
    else:
        # Fallback to polarity if no clear sentiment
        if polarity > 0.05:
            sentiment = "Positive"
        elif polarity < -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

    keywords = extract_keywords(text)
    emotion = detect_emotion(text)

    return sentiment, polarity, keywords, emotion, aspect_sentiments
