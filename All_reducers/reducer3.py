import sys
import math

current_word = None
current_count = 0
word = None
word_id = 1
total_documents = 0
tf_idf_dict = {}

for line in sys.stdin:
    line = line.strip()
    word, word_id, idf = line.split('\t', 2) # Split the line into word, word_id, and idf
    idf = float(idf) # Convert the IDF to a float
    
    # Calculate the TF-IDF for the word
    if current_word == word:
        current_count += 1
    else:
        if current_word:
            tf_idf = current_count / idf
            tf_idf_dict[word_id] = tf_idf
            print('%s\t%s\t%s' % (current_word, word_id, tf_idf))
        current_count = 1 
        current_word = word # Update the current word

# Output the last word
if current_word == word:
    tf_idf = current_count / idf
    tf_idf_dict[word_id] = tf_idf
    print('%s\t%s\t%s' % (word, word_id, tf_idf))
    
# Save tf_idf_dict to a file
with open('tf_idf_dict.txt', 'w') as f:
    for word_id, tf_idf in tf_idf_dict.items():
        f.write('%s\t%s\n' % (word_id, tf_idf))
        
