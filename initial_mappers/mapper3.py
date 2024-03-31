import sys

for line in sys.stdin:
    line = line.strip()
    word_id, idf = line.split('\t', 1)
    # print('%s\t%s' % (word_id, idf))
