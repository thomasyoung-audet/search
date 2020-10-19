import json
from timeit import default_timer as timer
import numpy as np
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from porter import PorterStemmer

"""
You need to write a program search for the retrieval process using the vector space model. 

The cosine similarity formula (with length normalization) should be used. 
Stop word removal and stemming could be turned on or off for both documents and queries. 

The input to this program would be a free text query (without Boolean operators), 
and the output would be a list of relevant documents together with their relevance scores. 

You may implement one (or more) of the top-K retrieval methods in which K is a predefined value, 
and in this case, the output will only be a list of K relevant documents with their relevance scores. 
"""


def lookup(input):
    use_stem = False
    stop_words = False
    g = open("postings.txt", "r")
    f = open("cacm.all", "r")
    content = g.read().replace('\n', ' ')
    if content[0] == "1":
        use_stem = True
    if content[1] == "1":
        stop_words = True
    post_list = json.loads("[" + content[2:-2] + "]")
    lines = f.readlines()
    f.close()
    extracted_postings = []
    docs = []
    final_list = []

    if g.mode == 'r':
        # get query
        # og_query = input("Enter query: ").lower()
        og_query = input
        og_query = re.sub('[^A-Za-z0-9$\- ]+', '', og_query)
        newquery = og_query.split()
        newquery.sort()
        if use_stem:
            stemmed_query = ""
            for word in newquery:
                p = PorterStemmer()
                word = p.stem(word, 0, len(word) - 1)
                stemmed_query += word
            newquery = stemmed_query

        term_list = get_term_lists(newquery, post_list)
        # remove duplicates if they exist
        term_list = list(dict.fromkeys(term_list))

        for entry in term_list:
            extracted_postings.append(post_list[entry])
        # get docs out of extracted postings
        for posting in extracted_postings:
            for entry in posting[1]:
                docs.append(entry[0])
        docs = list(dict.fromkeys(docs))
        docs.sort()
        document_vectors = get_doc_vector(docs, lines, use_stem, stop_words)

        # now, make all of those vectors have tf values, and then weights
        cosine_list = fill_vectors(document_vectors, og_query, docs)
        temp_list = []
        for i in range(len(docs)):
            temp_list.append([docs[i], cosine_list[i]])
        temp_list.sort(key=lambda x: x[1])
        temp_list.reverse()
        print("Query was: " + og_query + "\n")
        display(temp_list, get_doc_info(docs, lines))
        for elem in temp_list:
            final_list.append(elem[0])
        return final_list


def get_term_lists(query, post_list):
    term_list = []
    j = 0
    for i in range(len(post_list)):
        while query[j] == post_list[i][0]:
            term_list.append(i)
            j += 1
            if j == len(query):
                return term_list


def get_doc_vector(docs, lines, use_stem, use_stop_word):
    stop_words = []
    if use_stop_word:
        stop_words = open("stopwords.txt", "r").read().split('\n')
    i = 0
    document_text = ""
    documents = []
    start_scan = False
    scan_doc = False
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
                if use_stem:
                    word = stem(word)
                if use_stop_word:
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


def display(result_list, info_list):
    # display rank order, document title and document author
    # display 20 and ask to display all
    rank = 1
    for i in range(len(result_list)):
        if i == 20:
            continue_printing = input("\n Do you want to see the rest of the results?(Y/N)")
            if continue_printing == "N":
                return
        print("=======================")
        print(str(rank) + ". Document: " + str(result_list[i][0]))
        doc_entry = modified_binary_search(info_list, 0, len(info_list), result_list[i])
        print("Title: " + info_list[doc_entry][1])
        print("Author: " + info_list[doc_entry][2])
        rank += 1


def modified_binary_search(arr, left, right, x):
    # Check base case
    if right >= left:
        mid = left + (right - left) // 2
        # If element is present at the middle itself
        if arr[mid][0] == x[0]:
            return mid
            # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid][0] > x[0]:
            return modified_binary_search(arr, left, mid - 1, x)
            # Else the element can only be present
        # in right subarray
        else:
            return modified_binary_search(arr, mid + 1, right, x)
    else:
        # Element is not present in the array
        return -1


def get_doc_info(docs, lines):
    i = 0
    doc_title = ""
    doc_author = ""
    info_list = []
    start_scan = False
    scan_doc = False
    scan_bit = True
    for line in lines:
        if line.startswith("."):
            start_scan = False
        if line.startswith(".I " + str(docs[i])):
            scan_doc = True
        if start_scan is True and scan_doc is True:
            line = line.replace('\n', " ")
            if scan_bit:
                doc_title += line
            else:
                doc_author += line
        if line.startswith(".T") and scan_doc:
            start_scan = True
            scan_bit = True
        if line.startswith(".A") and scan_doc:
            start_scan = True
            scan_bit = False
        if line.startswith(".X") and scan_doc:
            scan_doc = False
            info_list.append([docs[i], doc_title, doc_author])
            doc_author = doc_title = ""
            if i < len(docs) - 1:
                i += 1
            else:
                break

    return info_list


def shutdown(return_times):
    acc = 0
    for times in return_times:
        acc += times
    if len(return_times) != 0:
        acc = acc / len(return_times)
        print("Average return time was: " + str(acc) + " seconds")
    else:
        print("No searches were made. Avg return time 0.")


def stem(word):
    p = PorterStemmer()
    return p.stem(word, 0, len(word) - 1)


if __name__ == "__main__":
    query = input("Enter query: ").lower()
    lookup(query)
