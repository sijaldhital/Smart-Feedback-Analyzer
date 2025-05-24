# Smart-Feedback-Analyzer

A sophisticated feedback analysis tool that provides sentiment analysis, emotion detection, and aspect-based insights using advanced NLP techniques.

Features

- Sentiment Analysis: Classifies feedback as Positive, Negative, Neutral, or Mixed
- Emotion Detection: Identifies emotions like Joy, Anger, Sadness, etc.
- Aspect-Based Analysis: Breaks down feedback by specific aspects/clauses
- Keyword Extraction: Identifies key phrases automatically
- Visual Dashboard: Clean, interactive results presentation
- Persistent Storage: Saves all analyses for historical review

Technology Stack

- Backend: Django REST Framework
- NLP Libraries:
  - TextBlob (Sentiment Analysis)
  - KeyBERT (Keyword Extraction)
  - Transformers (BERT for Aspect Sentiment)
  - Emotion Classification Model
- Frontend: Bootstrap 5 + Vanilla JS
- Database: SQLite (default)

