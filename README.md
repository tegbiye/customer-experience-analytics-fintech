# Customer Experience Analytics for Fintech Apps

## A Real-World Data Engineering Challenge: Scraping, Analyzing, and Visualizing Google Play Store Review

This repository contains a data pipeline to download that is scraping, cleaning, exploring, analyzing, and visualizing Google Play Store Reviews

---
## Project Structure

<pre>
|---- .github/
|     |--- workflows
|     |    |--- unittests.yml
|---- notebooks/
|     |--- README.md
|     |--- collect_preprocess.ipynb
|     |----sentiment_thematic_analysis.ipynb
|---- scripts/
|     |--- play_store_scraper.py
|     |--- preprocess.py
|     |----sentiment_analysis.py
|     |--- cleaned_review_data_insert.py
|     |----dump_files.py
|---- data/
|     |--- raw_data/
|     |    |---- CBE_review.csv
|     |    |---- BOA_review.csv
|     |    |---- DBE_review.csv
|     |--- cleaned_data/
|     |    |---- cleaned_review.csv
|     |    |-----sentiment_analysis_results.csv
|-----dumps/
|     |----README.MD
|     |----banks.sql (DDL and DML)
|     |----reviews.sql (DDL and DML)
|-----src/
|     |----__init__.py
|---- tests/
|     |--- __init__.py
|     |--- test_collect_preprocess.py
|     |--- test_play_store_scraper.py
|---- .gitignore
|---- requirements.txt
|----- LICENCE
|____ README.md
</pre>

---

## Project Objectives

**General goal:** Improve mobile Apps of to enhamce customer retention and satisfaction

**Specific Goals:**
  - Scrape User reviews from Google Play Store
  - Analyze sentiment (posetive, negative, and neutral) and extract themes
  - Identify satisfaction drivers and pain points
  - Store cleaned review data to the Oracle database
  - Deliver report with visualization and actionable recommendations
### Sentiment and Thematic Analysis
  Using the scripts sentiment_analysis.py
  Go over the notebook sentiment_thenatic_analysis.ipynb
### Store cleaned review data to the Oracle database
  load credentials from congig/oracle.env
  connect the database insert into database as explained in 
  cleaned_review_data_insert.py by running 
  ```
  python cleaned_review_data_insert.py
  ```
  Then to dump the DDL and DML statements
  ```
  python dump_files.py
  ```
## Getting Started

1. Clone the repository

 - git clone http://github.com/tegbiye/customer-experience-analytics-fintech.git
 - cd customer-experience-analytics-fintech

2. Create environment using venv
 python -m venv .venv

 - Activate the environment
   
   .venv\Scripts\activate
   
   source .venv\bin\activate
3. Install Dependencies

  pip install -r requirements.txt

📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute with proper attribution.
