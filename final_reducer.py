#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys
import re
import nltk
from nltk.corpus import stopwords
import math


# create vocabulary out of section text with each word having a unique id and save it to a file
def create_vocabulary():
    data = pd.read_csv("cleaned_dataset.csv", usecols=["SECTION_TEXT"])
    vocab = {}
    vocab_id = 1

    # turn section text into string first
    data["SECTION_TEXT"] = data["SECTION_TEXT"].apply(lambda x: str(x))
    for index, row in data.iterrows():
        words = row["SECTION_TEXT"].split()
        # create vocabulary
        for word in words:
            if word not in vocab:
                vocab[word] = vocab_id
                vocab_id += 1
    # save vocabulary to a file
    with open("vocabulary.txt", "w") as file:
        for word, id in vocab.items():
            file.write(f"{word} {id}\n")

    return vocab


vocab = create_vocabulary()
print("Vocabulary created")
print(vocab)


# calculate the term frequency in format article_id (word_id:frequency)
def calculate_term_frequency(vocab):
    data = pd.read_csv("sampled_data.csv", usecols=["ARTICLE_ID", "SECTION_TEXT"])
    term_freq_dict = {}

    with open("term_frequency.txt", "w") as file:
        for index, row in data.iterrows():
            article_id = row["ARTICLE_ID"]
            # converting to string first
            row["SECTION_TEXT"] = str(row["SECTION_TEXT"])
            words = row["SECTION_TEXT"].split()
            word_freq = {}

            for word in words:
                try:
                    word_id = vocab[word]
                    # new occurrence
                    if word_id not in word_freq:
                        word_freq[word_id] = 1
                    else:
                        # increment frequency
                        word_freq[word_id] += 1
                except KeyError:
                    # Handle the case when the word is not found in the vocab dictionary
                    # You can skip the word or handle it based on your requirements
                    continue

            term_freq_dict[article_id] = word_freq
            # store with format article_id (word_id:frequency)
            file.write(f"{article_id} ")
            for word_id, freq in word_freq.items():
                file.write(f"({word_id}:{freq}) ")
            file.write("\n")
    print("Term frequency calculated and saved to term_frequency.txt")
    return term_freq_dict


TF = calculate_term_frequency(vocab)


# calculate the inverse document frequency in format word_id (document_frequency)
def calculate_idf(vocab, term_freq_dict):
    idf_dict = {}
    total_documents = len(term_freq_dict)

    # calculate document frequency for each word and store in idf_dict
    for article_id, word_freq in term_freq_dict.items():
        for word_id in word_freq:
            if word_id not in idf_dict:
                idf_dict[word_id] = 1
            else:
                idf_dict[word_id] += 1

    return idf_dict


idf_dict = calculate_idf(vocab, TF)
print("IDF calculated")
print(idf_dict)


# store the idf values in a file
def store_idf(idf_dict):
    with open("idf.txt", "w") as file:
        file.write("word_id , doc_freq\n")
        for word_id, doc_freq in idf_dict.items():
            file.write(f"{word_id} {doc_freq}\n")
    print("IDF values saved to idf.txt")


store_idf(idf_dict)


# calculate the tf/idf values for each word in each document
def calculate_tf_idf(TF, idf_dict):
    tf_idf_dict = {}
    for article_id, word_freq in TF.items():
        tf_idf_dict[article_id] = {}
        for word_id, freq in word_freq.items():
            tf_idf = TF[article_id][word_id] / idf_dict[word_id]
            tf_idf_dict[article_id][word_id] = tf_idf

    # store tf-idf values in a file in format article_id (word_id, tf_idf)
    with open("tf_idf.txt", "w") as file:
        for article_id, word_freq in tf_idf_dict.items():
            file.write(f"{article_id} ")
            for word_id, tf_idf in word_freq.items():
                file.write(f"({word_id}, {tf_idf}) ")
            file.write("\n")

    return tf_idf_dict


tf_idf_dict = calculate_tf_idf(TF, idf_dict)
print("TF-IDF calculated")
print(tf_idf_dict)


# create vector for each ID
# if the word occurs in the ARTICLE_ID, the value is the tf-idf value of the word in the document otherwise 0
# this vector is calculated for each article_id
def create_vector():
    # key value of size of length of vocab
    vector = {}
    for article_id in tf_idf_dict:
        vector[article_id] = [0] * len(vocab)
        # if word exists in the article, set the value to the tf-idf value
        for word_id, tf_idf in tf_idf_dict[article_id].items():
            vector[article_id][word_id - 1] = tf_idf

    # store vector in a file
    with open("vector.txt", "w") as file:
        for article_id, vector_item in vector.items():
            file.write(f"{article_id} ")
            for value in vector_item:
                file.write(f"{value} ")
            file.write("\n")
    print("vector calculated and saved to query_vector.txt")
    return vector


vector_dict = create_vector()
print("vector created")
print(vector_dict)


# pre process the query, compute term freuqency and tf-idf values
# if the word exists in the vocab then take the qeury term frequency and divide it by dataset idf otherwise 0
# the query vector will be of size of the vocab of the dataset
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


def query_vector(query):
    query = clean_text(query)
    query = remove_stopwords(query)
    query = query.split()
    query_vector = [0] * len(vocab)

    for word in query:
        if word in vocab:
            word_id = vocab[word]
            query_vector[word_id - 1] = query.count(word) / idf_dict[word_id]

    # store query vector in a file
    with open("query_vector.txt", "w") as file:
        for value in query_vector:
            file.write(f"{value} ")
        file.write("\n")

    return query_vector


query = "The production coordinator serves under the production manager producer  or UPM to coordinate the various groups and personnel that come together in filmmaking to a movie and video production to make a television show."
query_vector = query_vector(query)
print("Query vector created")
print(query_vector)


# find relevance of the query with each document using the formula r(q, d) = ∑ qi⋅ di
# where qi is the ith element of the query vector and di is the ith element of the document vector
def calculate_relevance(query_vector, vector_dict):
    relevance_dict = {}

    # Convert query_vector to a numpy array
    query_vector = np.array(query_vector)

    for article_id, document_vector in vector_dict.items():
        # Convert document_vector to a numpy array
        document_vector = np.array(document_vector)

        # Find the indices of terms that exist in both the query and the document
        common_indices = np.intersect1d(
            np.nonzero(query_vector)[0], np.nonzero(document_vector)[0]
        )

        # Calculate the sum of the product of weights for these terms
        relevance = np.sum(
            query_vector[common_indices] * document_vector[common_indices]
        )

        # Store the relevance in the dictionary
        relevance_dict[article_id] = relevance

    # Sort the relevance dictionary by relevance values in descending order
    relevance_dict = dict(
        sorted(relevance_dict.items(), key=lambda item: item[1], reverse=True)
    )

    # store relevance values in a file
    with open("relevance.txt", "w") as file:
        for article_id, relevance in relevance_dict.items():
            file.write(f"{article_id} {relevance}\n")

    return relevance_dict


relevance_dict = calculate_relevance(query_vector, vector_dict)
print("Relevance calculated")
print(relevance_dict)


data = pd.read_csv("sampled_data.csv", usecols=["ARTICLE_ID", "SECTION_TEXT", "TITLE"])

top_relevant_documents = list(relevance_dict.items())[:5]

with open("top_relevant_documents.txt", "w") as file:
    for article_id, relevance in top_relevant_documents:
        article = data[data["ARTICLE_ID"] == article_id]
        file.write(f"Title: {article['TITLE'].values[0]}\n")
        file.write(f"Relevance: {relevance}\n")
        file.write(f"Content: {article['SECTION_TEXT'].values[0]}\n")
        file.write("\n")
