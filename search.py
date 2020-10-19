import json
from timeit import default_timer as timer
from porter import PorterStemmer
import numpy as np
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

"""
You need to write a program search for the retrieval process using the vector space model. 

The cosine similarity formula (with length normalization) should be used. 
Stop word removal and stemming could be turned on or off for both documents and queries. 

The input to this program would be a free text query (without Boolean operators), 
and the output would be a list of relevant documents together with their relevance scores. 

You may implement one (or more) of the top-K retrieval methods in which K is a predefined value, 
and in this case, the output will only be a list of K relevant documents with their relevance scores. 
"""


def search():
    return_times = []
    stem = "N"  # input("Was the stemmer used in the inversion? (Y/N)")
    stop_words = "N"  # input("Were stop words removed in the inversion? (Y/N)")
    g = open("postings.txt", "r")
    h = open("doc_lengths.txt", "r")
    f = open("test_cacm.all", "r")
    content = g.read().replace('\n', ' ')
    post_list = json.loads("[" + content[:-2] + "]")

    # I need to take the inverted list, and create a file that holds a document vector for each document in
    # the collection.
    extracted_postings = []
    query_vector = np.zeros(len(post_list))

    while g.mode == 'r' and h.mode == 'r':
        query = ""
        while query != "zzend":
            # calculate query vector
            og_query = "77 analysis technique noise"  # input("Enter a term to search for: ").lower()
            query = og_query.split()
            query.sort()
            if stem == "Y" or stem == "y":
                new_query = ""
                for word in query:
                    p = PorterStemmer()
                    word = p.stem(word, 0, len(word) - 1)
                    new_query += word
                query = new_query

            term_list = get_term_lists(query, post_list)
            # remove duplicates if they exist
            term_list = list(dict.fromkeys(term_list))

            for entry in term_list:
                extracted_postings.append(post_list[entry])
            # # get docs out of extracted postings
            docs = []
            for posting in extracted_postings:
                for entry in posting[1]:
                    docs.append(entry[0])
            docs = list(dict.fromkeys(docs))
            docs.sort()
            document_vectors = get_doc_vector(docs, f, stem, stop_words, post_list)

            # now, make all of those vectors have tf values, and then weights
            cosine_list = fill_vectors(document_vectors, og_query, docs)
            final_list = []
            for i in range(len(docs)):
                final_list.append([docs[i], cosine_list[i]])
            final_list.sort(key=lambda x: x[1])
            final_list.reverse()
            print("Query was: " + og_query)
            for item in final_list:
                print("Doc " + str(item[0]) + " with cosine similarity of " + str(item[1]))


def get_term_lists(query, post_list):
    term_list = []
    j = 0
    for i in range(len(post_list)):
        while query[j] == post_list[i][0]:
            term_list.append(i)
            j += 1
            if j == len(query):
                return term_list


def get_doc_vector(docs, f, stem, stop_words, postings):
    i = 0
    document_text = ""
    documents = []
    start_scan = False
    scan_doc = False
    if f.mode == 'r':
        lines = f.readlines()
        for line in lines:
            if line.startswith("."):
                start_scan = False
            if line.startswith(".I " + str(docs[i])):
                scan_doc = True
            if start_scan is True and scan_doc is True:
                words = str.split(line)
                for word in words:
                    # words are made lower case right from the start
                    word = word.lower()
                    word = re.sub('[^A-Za-z0-9$\-]+', '', word)
                    if stem == "Y":
                        word = stem(word)
                    if stop_words == "Y":
                        if not word in stop_words:
                            document_text += word + " "
                    else:
                        if word != '':
                            document_text += word + " "
            if (line.startswith(".T") or line.startswith(".W")) and scan_doc:
                start_scan = True
            if line.startswith(".B") and scan_doc == True:
                scan_doc = False
                documents.append(document_text)
                document_text = ""
                if i < len(docs) - 1:
                    i += 1
                else:
                    break

        return documents


def fill_vectors(documents, query, names):
    vectorizer = TfidfVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000,
                                 norm='l2',
                                 token_pattern=r"(?u)\b\w+\b")

    df1 = pd.DataFrame({"Query": [query]})
    i = 0
    for doc in documents:
        df2 = pd.DataFrame({"Doc " + str(names[i]): [doc]})
        df1 = df1.join(df2)
        i += 1
    # Initialize
    doc_vec = vectorizer.fit_transform(df1.iloc[0])
    # Create dataFrame
    df2 = pd.DataFrame(doc_vec.toarray().transpose(), index=vectorizer.get_feature_names())
    # Change column headers
    df2.columns = df1.columns
    arr = df2.to_numpy()
    query_vector = arr[:, 0]
    doc_matrix = np.delete(arr, 0, 1)
    cosine_matrix = (doc_matrix.T * query_vector).T
    cosine_similarity = cosine_matrix.sum(axis=0)
    return cosine_similarity


def shutdown(return_times):
    acc = 0
    for times in return_times:
        acc += times
    if len(return_times) != 0:
        acc = acc / len(return_times)
        print("Average return time was: " + str(acc) + " seconds")
    else:
        print("No searches were made. Avg return time 0.")


if __name__ == "__main__":
    search()
