# create query vector
import sys

# read the vocab and store the word_id and word in a dictionary
vocab = {}
with open('vocab.txt', 'r') as f:
    for line in f:
        word_id, word = line.strip().split('\t', 1)
        vocab[int(word_id)] = word
        
# read the idf_dict and store the word_id and idf in a dictionary
idf_dict = {}
with open('idf_dict.txt', 'r') as f:
    for line in f:
        word_id, idf = line.strip().split('\t', 1)
        idf_dict[int(word_id)] = float(idf)

query = "Your query goes here"
query = query.split()
# Initialize the query_vector
query_vector = [0] * len(vocab)

for line in sys.stdin:
    line = line.strip()
    word, word_id, tf_idf = line.split('\t', 2)
    tf_idf = float(tf_idf) 
    word_id = int(word_id)

    if word in query:
        query_vector[word_id - 1] = query.count(word) / idf_dict[word_id]

print('%s\t%s' % ("Query Vector", query_vector))

# save the query_vector to a file
with open('query_vector.txt', 'w') as f:
    f.write('%s\t%s\n' % ("Query Vector", query_vector))
    