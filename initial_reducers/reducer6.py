import sys
import numpy as np

# Read the query vector from the file
with open('query_vector.txt', 'r') as f:
    for line in f:
        query_vector = np.array([float(i) for i in line.split('\t', 1)[1].split()])        
 
relevance_dict = {}

for line in sys.stdin:
    line = line.strip()
    doc_id, document_vector = line.split('\t', 1)
    document_vector = np.array([float(i) for i in document_vector.split()])

    # Find the indices of terms that exist in both the query and the document
    common_indices = np.intersect1d(np.nonzero(query_vector)[0], np.nonzero(document_vector)[0])

    # Calculate the sum of the product of weights for these terms
    relevance = np.sum(query_vector[common_indices] * document_vector[common_indices])

    # Store the relevance in the dictionary
    relevance_dict[doc_id] = relevance

# Sort the relevance dictionary by relevance values in descending order
relevance_dict = dict(sorted(relevance_dict.items(), key=lambda item: item[1], reverse=True))

for doc_id, relevance in relevance_dict.items():
    print('%s\t%s' % (doc_id, relevance))
    
# Save the relevance_dict to a file
with open('relevance_dict.txt', 'w') as f:
    for doc_id, relevance in relevance_dict.items():
        f.write('%s\t%s\n' % (doc_id, relevance))