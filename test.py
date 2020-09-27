import json
from timeit import default_timer as timer

def test():
    return_times = []
    f = open("dictionary.txt", "r")
    content = f.read().replace('\n',' ')
    dict_list = json.loads("[" + content[:-2] + "]")
    g = open("postings.txt", "r")
    content = g.read().replace('\n', ' ')
    post_list = json.loads("[" + content[:-2] + "]")
    h = open("cacm.all", "r")
    lines = h.readlines()

    if f.mode == 'r' and g.mode == 'r' and h.mode == 'r':
        input_txt = ""
        while input_txt != "zzend":
            input_txt = input("Enter a term to search for: ").lower()
            # If the term is in one of the documents in the collection, the program should display the document
            # frequency
            # and all the documents which contain this term, for each document, it should display the document ID,
            # the title, the term frequency, all the positions the term occurs in that document, and a summary of the
            # document highlighting the first occurrence of this term with 10 terms in its context.
            # Each time, when user types in a valid term, the program should also output the time from getting the user
            # input to outputting the results. Finally, when the program stops, the average value for above-mentioned
            # time should also be displayed.

            # output doc freq: from dictionary.txt. I actually dont need this file at all. I could use len(docdata)
            # as a DF value. Is this bad?
            found = False
            start = timer()
            for elem in dict_list:
                if input_txt == elem[0]:
                    found = True
                    print("This term is found in " + str(elem[1]) + " documents.")
                    break
            if found:
                print("This search term is found in the following documents:")
                # output all docs that contain that term: DocID, title, TF, all the positions, first occurrence with 10
                # words
                docdata = []
                for entry in post_list:
                    if entry[0] == input_txt:
                        docdata += entry[1]
                        break
                # docdata now has doc ID, TF, and positions for each document input_txt appears in
                # now search in cacm for word data
                count = 0
                get_title_countdown = 0
                abstract_bool = False
                abstract_text = ""
                title = ""
                output = ""
                found = False
                for line in lines:
                    if get_title_countdown != 0:
                        get_title_countdown -= 1
                    if count == len(docdata):
                        break
                    if line.startswith(".I " + str(docdata[count][0])):
                        found = True
                        get_title_countdown = 3
                    if get_title_countdown == 1:
                        title = line
                    if line == ".B\n" and found:
                        abstract_bool = False
                        found = False
                        # I need to create the output string here, as its all going to be reset now.
                        output += "Document: - " + title + "Term frequency: " + str(docdata[count][1]) + "\n"\
                                  "First occurrence in document: " + \
                                  getcontext(title + abstract_text, docdata[count][2][0]) + "\n"
                        title = ""
                        abstract_text = ""
                        count += 1
                    if abstract_bool:
                        abstract_text += line
                    if line == ".W\n" and found:
                        abstract_bool = True

                end = timer()
                elapsed_time = (end - start)
                return_times += [elapsed_time]
                print(output)
                print("Search time: " + str(elapsed_time) + " seconds\n")

                # output time to results
            elif input_txt != "ZZEND":
                print("Term not found in any documents")
        shutdown(return_times)
        f.close()
        g.close()
        h.close()
    else:
        print("Error opening file. Try again.")
    # average value of return times should be returned


def getcontext(string, wordnum):
    word_list = string.split()
    if len(word_list) < 11:
        return string[:-1]
    elif wordnum < 5:
        return ' '.join(word_list[:10])
    elif wordnum > len(word_list)-10:
        return ' '.join(word_list[10:])
    else:
        return ' '.join(word_list[wordnum-5:wordnum+4])


def shutdown(return_times):
    acc = 0
    for times in return_times:
        acc += times
    if len(return_times) != 0:
        acc = acc / len(return_times)
        print("Average return time was:" + str(acc) + " seconds")
    else:
        print("No searches were made. Avg return time 0.")


if __name__ == "__main__":
    test()
