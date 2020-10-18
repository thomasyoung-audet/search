import json
from timeit import default_timer as timer
from porter import PorterStemmer
import numpy as np

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
    g = open("postings.txt", "r")
    content = g.read().replace('\n', ' ')
    post_list = json.loads("[" + content[:-2] + "]")

    # I need to take the inverted list, and create a file that holds a document vector for each document in
    # the collection.
    # OR
    # Say the query is "bal1 bla2 bla3", creates query Vector(1, 1, 1)
    # calculate idf value for bla1 bla2 and bla3
    # use inverted index to get all the docs with those three words (this would mean I would parse just 3 lines of
    # postings.txt) and create 3 term vectors for those documents.
    # calculate the TF value then the weight value for each entry
    # do normalization on the weights
    # calculate cosine similarity

    idf_list = []
    extracted_postings = []
    query_vector = np.zeros(len(post_list))

    while g.mode == 'r':
        query = ""
        while query != "zzend":
            # calculate query vector
            query = "1 01 0n 0n"  # input("Enter a term to search for: ").lower()
            query = query.split()
            query.sort()
            if stem == "Y" or stem == "y":
                new_query = ""
                for word in query:
                    p = PorterStemmer()
                    word = p.stem(word, 0, len(word) - 1)
                    new_query += word
                query = new_query

            term_list, query_vector = fill_query_vector(query, post_list, query_vector)
            # remove duplicates if they exist
            term_list = list(dict.fromkeys(term_list))

            # calculate tf, which is the same as w
            for term in term_list:
                query_vector[term] = 1 + np.log10(query_vector[term])

            # now for the document vectors
            # calculate idf values, get postings
            for entry in term_list:
                idf = np.log10(len(post_list) / (len(post_list[entry]) - 1))
                idf_list.append(idf)
                extracted_postings.append(post_list[entry])
            # turn into vectors for each document
            document_vectors = dict()

            for term_posting in extracted_postings:  # for each term
                for item in term_posting[1]:  # for each document
                    if item[0] in document_vectors:
                        document_vectors[item[0]][extracted_postings.index(term_posting)] += item[1]
                    else:
                        document_vectors[item[0]] = np.zeros(len(post_list))
                        document_vectors[item[0]][extracted_postings.index(term_posting)] = item[1]
            # now, make all of those vectors have tf values, and then weights
            # TODO need document lenghts
            for doc, vector in document_vectors.items():
                if doc != "idf":
                    for i in range(len(vector)):
                        if vector[i] != 0:
                            vector[i] = (1 + np.log10(vector[i])) * document_vectors["idf"][i]
            print("bla")

            # now for the cosine similarity
            # 1. query

def fill_query_vector(query, post_list, query_vector):
    term_list = []
    j = 0
    for i in range(len(post_list)):
        while query[j] == post_list[i][0]:
            term_list.append(i)
            query_vector[i] += 1
            j += 1
            if j == len(query):
                return term_list, query_vector


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
