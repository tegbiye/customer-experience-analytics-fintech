import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect


# Preprocessing function


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(
        word) for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)


def get_sentiment(text):
    """
    Placeholder function for sentiment analysis.
    Replace with actual sentiment analysis logic.
    """
    # For demonstration, return a dummy sentiment score
    analyzed = TextBlob(text)
    score = analyzed.sentiment.polarity
    if score > 0:
        label = 'positive'
    elif score < 0:
        label = 'negative'
    else:
        label = 'neutral'
    return {'label': label, 'score': score}


def get_sentiment_vader(text, sia):
    """
    Placeholder function for sentiment analysis using VADER.
    Replace with actual sentiment analysis logic.
    """
    # For demonstration, return a dummy sentiment score
    scores = sia.polarity_scores(text)['compound']
    if scores > 0:
        label = 'positive'
    elif scores < 0:
        label = 'negative'
    else:
        label = 'neutral'
    return {'label': label, 'score': scores}


def is_amharic(text):
    """
    Placeholder function for language detection.
    Replace with actual language detection and logic.
    """
    # For demonstration, return the original text
    return any('\u1200' <= char <= '\u137F' for char in text)


def get_sentiment_score(text, bert_model, sentiment_model):
    """
    Function to get sentiment score using VADER.
    """
    if is_amharic(text) == True:
        lang_text = bert_model(text)
    else:
        lang_text = sentiment_model(text)
    return lang_text[0]['score'] if lang_text[0]['label'] == 'POSITIVE' else 1 - lang_text[0]['score']


def classify_sentiments_with_label_neutral(texts, amharic_model, default_model, neutral_threshold=0.05):
    """
    Classify texts using language-specific sentiment models.
    Supports 'positive', 'neutral', and 'negative' using score comparison logic.

    Args:
        texts (list): List of review texts.
        amharic_model (callable): Sentiment model for Amharic.
        default_model (callable): Sentiment model for other languages.
        neutral_threshold (float): Margin to detect neutrality if top scores are close.

    Returns:
        list of dict: Each dict contains 'label' and 'score'.
    """
    results = []

    for text in texts:
        try:
            prediction = amharic_model(text) if is_amharic(
                text) else default_model(text)
        except Exception as e:
            results.append({'label': 'error', 'score': 0.0, 'error': str(e)})
            continue

        if isinstance(prediction, list) and isinstance(prediction[0], dict):
            if len(prediction) == 1:
                # Single-label output
                label = prediction[0]['label'].lower()
                score = round(prediction[0]['score'], 4)
            else:
                # Multi-label output: check top two scores
                normalized = [{**p, 'label': p['label'].lower()}
                              for p in prediction]
                sorted_preds = sorted(
                    normalized, key=lambda x: x['score'], reverse=True)
                top1, top2 = sorted_preds[0], sorted_preds[1]

                if abs(top1['score'] - top2['score']) <= neutral_threshold:
                    label = 'neutral'
                    score = round((top1['score'] + top2['score']) / 2, 4)
                else:
                    label = top1['label']
                    score = round(top1['score'], 4)

            results.append({'label': label, 'score': score})
        else:
            results.append({'label': 'unknown', 'score': 0.0})

    return results


def map_keywords_to_themes(keywords: list, themes_map: dict) -> list:
    """
    Map keywords to themes based on a predefined mapping.

    Args:
        keywords (list): List of keywords to map.
        themes_map (dict): Dictionary mapping keywords to themes.

    Returns:
        list: List of themes corresponding to the keywords.
    """
    mapped_themes = []
    for keyword in keywords:
        theme = themes_map.get(keyword, 'Other')
        mapped_themes.append(theme)
    return mapped_themes
