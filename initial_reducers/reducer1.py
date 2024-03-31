import sys

vocab = {}
TF = {}
current_word = None
current_count = 0
word = None
word_id = 1

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)  # Split the line into word and count
    count = int(count)
    # If the word is the same as the current word, increment the count
    if current_word == word:
        current_count += count
    else:
        if current_word:
            vocab[word_id] = current_word
            TF[word_id] = current_count
            word_id += 1  # Increment the word ID
        # Update the current word and count
        current_count = count
        current_word = word

# Output the last word
if current_word == word:
    vocab[word_id] = current_word
    TF[word_id] = current_count

# save the vocab to a file
with open('vocab.txt', 'w') as f:
    for word_id, word in vocab.items():
        f.write('%s\t%s\n' % (word_id, word))
        
# save the TF to a file
with open('TF.txt', 'w') as f:
    for word_id, count in TF.items():
        f.write('%s\t%s\n' % (word_id, count))
        