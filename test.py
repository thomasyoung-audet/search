import json
return_times = []


def test():
    f = open("dictionary.txt", "r")
    contents = f.read()
    dict_list = json.loads(contents)
    g = open("postings.txt", "r")
    post_list = json.loads(contents)
    h = open("cacm.all", "r")

    input_txt = ""
    while input_txt != "ZZEND":
        input_txt = input("Enter a term to search for:")
        # If the term is in one of the documents in the collection, the program should display the document frequency
        # and all the documents which contain this term, for each document, it should display the document ID,
        # the title, the term frequency, all the positions the term occurs in that document, and a summary of the
        # document highlighting the first occurrence of this term with 10 terms in its context.
        # Each time, when user types in a valid term, the program should also output the time from getting the user
        # input to outputting the results. Finally, when the program stops, the average value for above-mentioned
        # time should also be displayed.

        # output doc freq: from dictionary.txt
        for elem in dict_list:
            if input_txt == elem[0]:
                print("Document frequency: " + elem[1])

        # output all docs that contain that term: DocID, title, TF, all the positions, first occurrence with 10 words
        docdata = []
        for entry in post_list:
            if entry[0] == input_txt:
                for data in entry[1]:
                    docdata += [data[0], data[1], data[2]]


        # output time to results


    f.close()
    g.close()
    h.close



        # average value of return times should be returned

def shutdown():
    acc = 0
    for times in return_times:
        acc += times
    if len(return_times) != 0:
        acc = acc/len(return_times)
        print("Average return time was:" + str(acc))
    else:
        print("No searches were made. Avg return time 0.")


if __name__ == "__main__":
    test()