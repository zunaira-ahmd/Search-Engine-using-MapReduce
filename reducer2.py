import sys
import math

# Initialize variables
current_word = None
current_count = 0
word = None
word_id = 1
total_documents = 0
idf_dict = {}

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1) 
    count = int(count)
    
    # Calculate the IDF for the word
    if current_word == word:
        current_count += count
    else:
        if current_word:
            idf = math.log(total_documents / current_count)
            idf_dict[word_id] = idf
            print('%s\t%s\t%s' % (current_word, word_id, idf))
            word_id += 1
        current_count = count
        current_word = word
        total_documents += 1

# Output the last word
if current_word == word:
    idf = math.log(total_documents / current_count)
    idf_dict[word_id] = idf
    print('%s\t%s\t%s' % (current_word, word_id, idf))

# Save idf_dict to a file
with open('idf_dict.txt', 'w') as f:
    for word_id, idf in idf_dict.items():
        f.write('%s\t%s\n' % (word_id, idf))
