import json
from timeit import default_timer as timer
from porter import PorterStemmer
import math

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

    while g.mode == 'r':
        query = ""
        while query != "zzend":
            # calculate query vector
            query = "the the same string"  # input("Enter a term to search for: ").lower()
            query = query.split()
            query.sort()
            query_dict = dict()
            query_vector = []
            for word in query:
                if stem == "Y" or stem == "y":
                    p = PorterStemmer()
                    word = p.stem(word, 0, len(word) - 1)
                if word in query_dict:
                    if query_dict[word] > 0:
                        query_dict[word] += 1
                else:
                    query_dict[word] = 1
            # calculate tf, w, and create vector
            for word, value in sorted(query_dict.items()):
                query_dict[word] = 1 + math.log10(query_dict[word])
                query_vector.append(query_dict[word])
                query_dict[word] = 0

            # now for the document vectors
            # calculate idf values, get postings
            for entry in post_list:
                if entry[0] in query_dict:
                    idf = math.log10(len(post_list) / (len(entry[1]) - 1))
                    entry.append(idf)
                    query_dict[entry[0]] = entry
            # turn into vectors for each document
            document_vectors = dict()
            i = -1
            for term, term_posting in sorted(query_dict.items()):  # for each term
                i += 1
                for item in term_posting[1]:  # for each document
                    if item[0] in document_vectors:
                        document_vectors[item[0]][i] += item[1]
                    else:
                        document_vectors[item[0]] = [0, 0, 0]
                        document_vectors[item[0]][i] = item[1]
            # now, make all of those vectors have tf values, and then weights
            # TODO need document lenghts
            


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
