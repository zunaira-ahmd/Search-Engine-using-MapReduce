# creates vector representation of the documents and saves it to a file
import sys

current_doc = None
doc_vector = [] 
# read the vocab and store the word_id and word in a dictionary
vocab = {}
with open('vocab.txt', 'r') as f:
    for line in f:
        word_id, word = line.strip().split('\t', 1)
        vocab[int(word_id)] = word

for line in sys.stdin:
    line = line.strip()
    doc_id, word_id, tf_idf = line.split('\t', 2)
    tf_idf = float(tf_idf)
    word_id = int(word_id)

    # Initialize the doc_vector if it is the first word
    if current_doc == doc_id:
        doc_vector[word_id - 1] = tf_idf # Subtract 1 to account for 0-based indexing
    # If the doc_id changes, print the doc_vector and reset it
    else:
        if current_doc:
            print('%s\t%s' % (current_doc, doc_vector))
        current_doc = doc_id
        doc_vector = [0] * len(vocab)
        doc_vector[word_id - 1] = tf_idf

# Output the last doc_vector
if current_doc == doc_id:
    print('%s\t%s' % (current_doc, doc_vector))
    
# save the doc_vector to a file
with open('doc_vector.txt', 'w') as f:
    for doc_id, doc_vector in enumerate(doc_vector):
        f.write('%s\t%s\n' % (doc_id, doc_vector))
        