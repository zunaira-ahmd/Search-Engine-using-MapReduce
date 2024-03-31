#!/usr/bin/env python3

import sys
import re
import nltk
import pandas as pd
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Remove special characters and digits
    text = re.sub(r"\s+[a-zA-Z]\s+", " ", text)
    # Single character removal
    text = re.sub(r"\s+", " ", text, flags=re.I)
    # Removing prefixed 'b'
    text = re.sub(r"^b\s+", "", text)
    # Converting to Lowercase
    text = re.sub(r"[^a-zA-Z]", " ", text)
    
    return text


def remove_stopwords(text):
    words = text.split()
    cleaned_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(cleaned_words)

cleaned_data = []

# Counter for generating ARTICLE_ID
article_id_counter = 1

for line in sys.stdin:
    line = line.strip()
    line = line.lower()
    line = remove_stopwords(line)
    line = clean_text(line)
    # Append the cleaned line along with ARTICLE_ID to the cleaned data
    cleaned_data.append({"ARTICLE_ID": article_id_counter, "SECTION_TEXT": line})
    article_id_counter += 1

# Create DataFrame from the cleaned data
data = pd.DataFrame(cleaned_data)

# Save cleaned data to CSV file
data.to_csv("cleaned_dataset.csv", index=False)
print("data saved")

