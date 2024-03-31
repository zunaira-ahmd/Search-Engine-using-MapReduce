# Search Engine using MapReduce
Search engines are the cornerstones of the modern web, allowing us to find relevant information within a vast sea of data. Building a scalable search engine requires handling massive datasets and complex algorithms. MapReduce, a distributed programming paradigm, provides a powerful framework for parallelizing the process of building and querying a search index across many clusters of computers.

### **Dependencies**
* Jupyter Notebook
* Apache Hadoop


# Introduction
Our aim is to create a simplified search engine. Search engines are remarkable examples of systems that manage enormous datasets with minimal latency.  A common search engine indexes millions of documents and must rapidly handle a massive influx of queries, returning the most relevant results in near real-time.  At its heart, information retrieval is the task of pinpointing relevant information. This breaks down into document indexing and query processing.  Indexing can be performed offline in a batch-like manner, while query processing demands immediate responses. The MapReduce paradigm in Hadoop provides a suitable framework for indexing large text collections beyond the capabilities of a single machine. For this assignment, we implemented a basic version of both components using MapReduce.

# Information Retrieval for Text
Before we can delve into information retrieval, we need to clean the data. This preprocessing involves removing stopwords (common words like "the"), symbols, excess whitespace, and punctuation. With clean data, we can begin the core steps of retrieving and organizing information.

### Term Frequency (TF)
We start by building a vocabulary of every unique word found in your 'SECTION_TEXT', assigning each word a unique ID.  Term frequency (TF) tells us how often a specific word appears within a document (see example image below).

### Inverse Document Frequency (IDF)
Alongside TF, we calculate IDF for each word. Inverse Document Frequency (IDF)  indicates how many documents a word appears in, revealing how common or unique a  term is. Words with high IDF values are less distinctive across the dataset.  An example format might be (word_id, doc_freq), as shown below.

### TF-IDF Weights
TF-IDF weights combine term frequency with Inverse Document Frequency normalization. While there are different TF-IDF calculation methods, in this assignment,  we divide each document's term frequency by the corresponding word's IDF. This gives us TF-IDF values for each word within each document.

# Basic Vector Space Model
The basic vector space model represents documents and queries as vectors based on their TF-IDF weights.  A simple way to create these vectors is to use the word ID as the index and store the corresponding TF-IDF value.  For example, a document with a vocabulary-sized vector might look like this:

[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


