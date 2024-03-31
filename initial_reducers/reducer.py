import sys
import ast
import math

def word_enumeration_reducer():
    current_word = None
    word_id = 1  # Starting ID for words

    for line in sys.stdin:
        word, _ = line.strip().split('\t', 1)
        if current_word != word:
            if current_word:
                print(f"{current_word} {word_id}")
                word_id += 1
            current_word = word

def document_count_reducer():
    current_word = None
    total_documents = 0

    for line in sys.stdin:
        word, count = line.strip().split('\t', 1) 
        count = int(count) 

        if current_word != word:
            if current_word:
                print(f"{current_word} {total_documents}")
            current_word = word
            total_documents = count
        else:
            total_documents += count

    if current_word:
        print(f"{current_word} {total_documents}")

def indexer_reducer():
    current_doc_id = None
    tfidf_values = {}

    for line in sys.stdin:
        doc_id, values_str = line.strip().split('\t', 1)
        values = ast.literal_eval(values_str) 

        if current_doc_id != doc_id: 
            if current_doc_id:
                print(f"{current_doc_id} {tfidf_values}")
            current_doc_id = doc_id
            tfidf_values = values
        else:
            tfidf_values.update(values)

    if current_doc_id:
        print(f"{current_doc_id} {tfidf_values}")

def query_processing_reducer(query_vector):
    query = ast.literal_eval(query_vector)
    query_magnitude = sum(value ** 2 for value in query.values())
    scores = {}

    for line in sys.stdin:
        doc_id, tfidf_values_str = line.strip().split('\t', 1)
        tfidf_values = ast.literal_eval(tfidf_values_str)
        dot_product = sum(query.get(word_id, 0) * tfidf for word_id, tfidf in tfidf_values.items()) 
        doc_magnitude = sum(tfidf ** 2 for tfidf in tfidf_values.values()) 
        relevance = dot_product / (math.sqrt(query_magnitude) * math.sqrt(doc_magnitude)) 
        scores[doc_id] = relevance

    sorted_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for doc_id, relevance in sorted_documents:
        print(f"{doc_id} {relevance}")

if __name__ == "__main__":
    if sys.argv[1] == "word_enumeration":
        word_enumeration_reducer()
    elif sys.argv[1] == "document_count":
        document_count_reducer()
    elif sys.argv[1] == "indexer":
        indexer_reducer()
    elif sys.argv[1] == "query_processing":
        query_vector = sys.argv[2]  # Pass query vector as argument
        query_processing_reducer(query_vector)


