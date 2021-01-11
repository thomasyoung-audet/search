Program that implements a vector space model information retrieval system. Uses TF-IDF weighting schemes to normalize document length and term frequency. Corpus used is a collection of papers and their abstracts (cacm.all file). Auto-Calculates evaluation metrics. 
```
cacm.all               text of documents
cite.info              key to citation info (the X sections in cacm.all)
common_words           stop words used by smart
qrels.text             relation giving qid did 0 0 to indicate dument did is  relevant to query qid
query.text             Original text of the query
```
