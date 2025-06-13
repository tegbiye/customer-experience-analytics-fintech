import cx_Oracle
import pandas as pd
from dotenv import dotenv_values
ENV_PATH = "config/oracle.env"
OR_CRED = dotenv_values(ENV_PATH)
# Oracle DB connection info
username = OR_CRED.get('ORACLE_USER')
password = OR_CRED.get('ORACLE_PASSWORD')
host = OR_CRED.get('ORACLE_HOST')
port = OR_CRED.get('ORACLE_PORT')
# Replace with your actual PDB name
service_name = OR_CRED.get('ORACLE_SERVICE_NAME')

dsn = cx_Oracle.makedsn(host, port, service_name=service_name)

conn = cx_Oracle.connect(username, password, dsn)
cursor = conn.cursor()

# Dump banks
df_banks = pd.read_sql("SELECT * FROM banks", conn)
with open("banks.sql", "w", encoding="utf-8") as f:
    for _, row in df_banks.iterrows():
        name = str(row['BANK_NAME']).replace("'", "''")  # Escape single quotes
        f.write(
            f"INSERT INTO banks (bank_id, bank_name) VALUES ({row['BANK_ID']}, '{name}');\n")
# Dump reviews (optional - remove large text if not needed)
df_reviews = pd.read_sql("SELECT * FROM reviews", conn)
df_reviews.columns = [col.lower()
                      for col in df_reviews.columns]  # Normalize column names

with open("reviews.sql", "w", encoding="utf-8") as f:
    for _, row in df_reviews.iterrows():
        # Safely handle text fields (escape quotes)
        processed = str(row['processed_review']).replace(
            "'", "''") if row['processed_review'] else ''
        keywords = str(row['keywords']).replace(
            "'", "''") if row['keywords'] else ''
        themes = str(row['themes']).replace("'", "''") if row['themes'] else ''

        # Optional: Handle null ratings and scores (avoid writing 'nan')
        def safe_num(val):
            return "NULL" if pd.isna(val) else val

        f.write(f"""INSERT INTO reviews (
    review_id, bank_id, processed_review, review_date, rating,
    sentiment, sentiment_score, vader_sentiment, vader_sentiment_score,
    sentiment_hf, sentiment_hf_score, keywords, themes
) VALUES (
    {row['review_id']}, {row['bank_id']}, '{processed}', TO_DATE('{row['review_date']}', 'YYYY-MM-DD'), {safe_num(row['rating'])},
    '{row['sentiment']}', {safe_num(row['sentiment_score'])}, '{row['vader_sentiment']}', {safe_num(row['vader_sentiment_score'])},
    '{row['sentiment_hf']}', {safe_num(row['sentiment_hf_score'])}, '{keywords}', '{themes}'
);\n""")

conn.close()
