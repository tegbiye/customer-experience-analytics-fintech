import cx_Oracle
import pandas as pd

# Load your DataFrame
# replace with actual source
df = pd.read_csv(
    "C:\\Users\\Tegbabu\\customer-experience-analytics-fintech\\data\\cleaned_data\\sentiment_analysis_results.csv")


# Convert dates to proper format
df['review_date'] = pd.to_datetime(
    df['review_date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Drop rows where 'processed_review' is missing (NaN or None)
df = df.dropna(subset=['processed_review'])


# Oracle DB connection info
username = "bank_reviews"
password = "Oracle123"
dsn = "localhost:1521/XEPDB1"  # Replace with your actual PDB name

# Connect to Oracle
conn = cx_Oracle.connect(username, password, dsn)
cur = conn.cursor()

# Insert unique banks and get their IDs
bank_name_id_map = {}
for bank in df['bank_name'].dropna().unique():
    bank_id_var = cur.var(cx_Oracle.NUMBER)
    cur.execute("""
        INSERT INTO banks (bank_name)
        VALUES (:1)
        RETURNING bank_id INTO :2
    """, (bank, bank_id_var))
    bank_id = int(bank_id_var.getvalue()[0])
    bank_name_id_map[bank] = bank_id

# Insert reviews
for _, row in df.iterrows():
    bank_id = bank_name_id_map.get(row['bank_name'])
    if not bank_id:
        continue  # Skip if bank not found (shouldn't happen)

    cur.execute("""
        INSERT INTO reviews (
            bank_id, processed_review, review_date, rating,
            sentiment, sentiment_score,
            vader_sentiment, vader_sentiment_score,
            sentiment_hf, sentiment_hf_score,
            keywords, themes
        ) VALUES (
            :1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4,
            :5, :6, :7, :8, :9, :10, :11, :12
        )
    """, (
        bank_id,
        row['processed_review'],
        row['review_date'],
        row['rating'],
        row['sentiment'],
        row['sentiment_score'],
        row['vader_sentiment'],
        row['vader_sentiment_score'],
        row['sentiment_hf'],
        row['sentiment_hf_score'],
        row['keywords'],
        row['themes']
    ))

# Commit changes and close
conn.commit()
cur.close()
conn.close()

print("✅ Review data inserted successfully.")
