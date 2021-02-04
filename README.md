# Search

Program that implements a vector space model information retrieval system. Uses TF-IDF weighting schemes to normalize document length and term frequency. Corpus used is a collection of papers and their abstracts (cacm.all file). Auto-Calculates evaluation metrics. 
```
cacm.all               text of documents
stopwords.txt          stop words that can be ignored by the program during the inverted index creation
===evaluation files===
query.text             Original text of the query
qrels.text             relation giving qid did 0 0 to indicate document did is relevant to query qid
```

## How to run

1. execute ```python3 invert.py``` to create the inverted index file. It will ask you if you want to ignore stop words and use the stemmer.
2. execute ```python3 search.py``` to run a query of your choice on the document collection. 
3. execute ```python3 eval.py``` to run the automatic evaluation program. This uses the queries in query.text, and evaluates the search program against the lists of relevant docs given in qrels.text to give Mean Average Procision and R-Precision values.
