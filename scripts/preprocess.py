# Import necessary libraries
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file and return its content as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return []


def preprocess_text(text):
    """
    Preprocess the input text by removing extra spaces and converting to lowercase.

    Args:
        text (str): The input text to preprocess.

    Returns:
        str: The preprocessed text.
    """
    # Remove extra spaces
    tokens = word_tokenize(text.lower())
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(
        word) for word in tokens if word.isalnum() and word not in stop_words]

    return ' '.join(tokens)


def clean_data(df):
    """
    Clean the DataFrame by preprocessing the 'review_text' column.

    Args:
        df (pd.DataFrame): The DataFrame containing the reviews.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df['review_text'] = df['review_text'].astype(str).str.strip()
    df['bank_name'] = df['bank_name'].astype(str).str.strip()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['source'] = df['source'].astype(str).str.strip()

    # Drop missing or duplicate values
    df.dropna(subset=['review_text', 'bank_name',
              'date', 'source'], inplace=True)
    df.drop_duplicates(
        subset=['review_text', 'bank_name', 'date', 'source'], inplace=True)
    return df


def balance_review(df, count=400):
    """
    Balance the number of reviews for each bank to a specified count.

    Args:
        df (pd.DataFrame): The DataFrame containing the reviews.
        count (int): The target number of reviews for each bank.

    Returns:
        pd.DataFrame: The balanced DataFrame.
    """
    banks = df['bank_name'].unique()
    balanced_df = pd.DataFrame()

    for bank in banks:
        bank_reviews = df[df['bank_name'] == bank]
        if len(bank_reviews) > count:
            bank_reviews = bank_reviews.sample(n=count, random_state=42)
        elif len(bank_reviews) < count:
            # If not enough reviews, repeat some to reach the count
            bank_reviews = bank_reviews.sample(
                n=count, replace=True, random_state=42)
        balanced_df = pd.concat([balanced_df, bank_reviews])

    return balanced_df.reset_index(drop=True)


def combine_dataframes(dataframes):
    """
    Combine multiple DataFrames into one.

    Args:
        dataframes (list): A list of DataFrames to combine.

    Returns:
        pd.DataFrame: The combined DataFrame.
    """
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df


def save_cleand_data(df, file_path):
    """
    Save the cleaned DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        file_path (str): The path where the CSV file will be saved.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Cleaned data saved to {file_path}")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")
