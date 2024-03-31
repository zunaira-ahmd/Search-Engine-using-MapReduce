# Search Engine using MapReduce
Search engines are the cornerstones of the modern web, allowing us to find relevant information within a vast sea of data. Building a scalable search engine requires handling massive datasets and complex algorithms. MapReduce, a distributed programming paradigm, provides a powerful framework for parallelizing the process of building and querying a search index across many clusters of computers.

### **Dependencies**
* Jupyter Notebook
* Apache Hadoop


# Introduction
Our aim is to create a simplified search engine. Search engines are remarkable examples of systems that manage enormous datasets with minimal latency.  A common search engine indexes millions of documents and must rapidly handle a massive influx of queries, returning the most relevant results in near real-time.  At its heart, information retrieval is the task of pinpointing relevant information. This breaks down into document indexing and query processing.  Indexing can be performed offline in a batch-like manner, while query processing demands immediate responses. The MapReduce paradigm in Hadoop provides a suitable framework for indexing large text collections beyond the capabilities of a single machine. For this assignment, we implemented a basic version of both components using MapReduce.

# Information Retrieval for Text:
First off, the data is cleaned by performing pre-processing steps which include removing of stopwords, symbols, extra whitespaces, puncuation marks etc. After the cleaning of data, bsic steps are followed to retrieve maximum information and to sort out the vast data.
A vocabulary is created consisting of every word in the 'SECTION_TEXT' with a unique ID for each word. To compute TF - term frequency 
