import search
import re
from porter import PorterStemmer

"""
The final part of the assignment is to evaluate the performance of the IR system you have developed. 
You need to write a program eval. The input to this program would be query.text and qrels.text from CACM. 
Your program should go through all the queries in query.text, for each query, get all the relevant results 
from your system (by running search), compare the results with the actual user judgment from qrels.text, 
and then calculate the mean average precision (MAP) and R-Precision values. 

The final output will be the average MAP and R-Precision values over all queries. 
"""


def evaluate(K):
    stem = False
    stop_words = False
    g = open("postings.txt", "r")
    check = g.read().replace('\n', ' ')
    if check[0] == "1":
        stem = True
    if check[1] == "1":
        stop_words = True
    g.close()

    q = open("query.text", "r")
    query_content = q.readlines()
    q.close()
    querylist = get_queries(query_content, stem, stop_words)

    rels = open("qrels.text", "r")
    rel_context = rels.read().replace('\n', ' ').split()
    g.close()
    rel_context = list(filter('0'.__ne__, rel_context))
    rel_context = [int(x) for x in rel_context]
    relevance_dict = dict.fromkeys(range(1, len(querylist) + 1))
    i = 1
    while i < len(rel_context):
        if relevance_dict[rel_context[i - 1]] is None:
            relevance_dict[rel_context[i - 1]] = []
        relevance_dict[rel_context[i - 1]].append(rel_context[i])
        i += 2

    result_list = []
    i = 1
    for query in querylist:
        print("Creating result list for query #" + str(i))
        result_list.append(search.lookup(query, False, K))
        i += 1
    # query = 'Articles on text formatting systems, including "what you see is what you get" systems.  Examples: t/nroff, scribe, bravo.'
    # result_list.append(search.lookup(query, False, 40))
    # calculate Mean Average Precision and R-precision
    # calculate average precision for each query, then average those
    print("==========================")
    print("calculating MAP/R-P")
    average_precisions = []
    r_precisions = []
    for i in range(len(result_list)):
        print("Query #" + str(i + 1))
        if relevance_dict[i+1] is not None:
            average_precisions.append(get_avg_prec(result_list[i], relevance_dict[i + 1])[0])
            r_precisions.append(get_avg_prec(result_list[i], relevance_dict[i + 1])[1])
            print("Average precision: " + str(average_precisions[-1]))
            print("R precision: " + str(r_precisions[-1]))
        else:
            print("No relevant document list was provided, no calculations can be made")
    MAP = sum(average_precisions) / len(average_precisions)
    R_PREC = sum(r_precisions) / len(r_precisions)

    print("\nMAP is: " + str(MAP))
    print("Average R-Precision is: " + str(R_PREC))


def get_avg_prec(query_results, relevant_results):
    relevant_found = 0
    r_counter = 0
    total_found = 0
    precision_history = []
    i = 0
    for result in query_results:
        i += 1
        if result in relevant_results:
            relevant_found += 1
            if i < len(query_results):
                r_counter += 1
        total_found += 1
        precision_history.append(relevant_found / total_found)

    r_precision = r_counter / len(query_results)
    return [sum(precision_history) / len(relevant_results), r_precision]


def get_queries(lines, use_stem, use_stop_word):
    stop_words = []
    if use_stop_word:
        stop_words = open("stopwords.txt", "r").read().split('\n')
    query_text = ""
    queries = []
    start_scan = False
    for line in lines:
        if line.startswith("."):
            start_scan = False
        if start_scan is True:
            words = str.split(line)
            for word in words:
                # words are made lower case right from the start
                word = word.lower()
                word = re.sub('[^A-Za-z0-9$\-]+', '', word)
                if use_stem:
                    word = stem(word)
                if use_stop_word:
                    if word not in stop_words:
                        query_text += word + " "
                else:
                    if word != '':
                        query_text += word + " "
        if line.startswith(".W"):
            start_scan = True
        if line.startswith(".N"):
            queries.append(query_text)
            query_text = ""

    return queries


def stem(word):
    p = PorterStemmer()
    return p.stem(word, 0, len(word) - 1)


if __name__ == "__main__":
    K = 20
    evaluate(K)
