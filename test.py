import json
from timeit import default_timer as timer
from porter import PorterStemmer


def test():
    stem = input("Was the stemmer used in the inversion? (Y/N)")
    return_times = []
    g = open("postings.txt", "r")
    content = g.read().replace('\n', ' ')
    post_list = json.loads("[" + content[:-2] + "]")
    h = open("cacm.all", "r")
    lines = h.readlines()

    if g.mode == 'r' and h.mode == 'r':
        word = ""
        while word != "zzend":
            word = input("Enter a term to search for: ").lower()
            if stem == "Y":
                p = PorterStemmer()
                word = p.stem(word, 0, len(word) - 1)

            found = False
            start = timer()
            for elem in post_list:
                if word == elem[0]:
                    found = True
                    print("\nThis term is found in " + str(len(elem[1])) + " documents.")
                    print("=============================================================================")
                    break
            if found:
                print("This search term is found in the following documents:\n")
                # output all docs that contain that term: DocID, title, TF, all the positions, first occurrence with 10
                # words
                docdata = []
                for entry in post_list:
                    if entry[0] == word:
                        docdata += entry[1]
                        break
                # docdata now has doc ID, TF, and positions for each document input_txt appears in
                # now search in cacm for word data
                count = 0
                get_title = False
                abstract_bool = False
                abstract_text = ""
                title = ""
                output = ""
                found = False
                for line in lines:
                    if count == len(docdata):
                        break
                    if line.startswith(".I " + str(docdata[count][0])):
                        found = True
                    if line == ".B\n" and found:
                        get_title = False
                        abstract_bool = False
                        found = False
                        # I need to create the output string here, as its all going to be reset now.
                        output += "Document: - " + title + "Term frequency: " + str(docdata[count][1]) + "\n"\
                                  "First occurrence in document: " + \
                                  getcontext(title + abstract_text, docdata[count][2][0]) + "\n" + "------------" + "\n"
                        title = ""
                        abstract_text = ""
                        count += 1
                    if abstract_bool:
                        abstract_text += line
                    if line == ".W\n" and found:
                        get_title = False
                        abstract_bool = True
                    if get_title:
                        title += line
                    if line == ".T\n" and found:
                        get_title = True

                end = timer()
                elapsed_time = (end - start)
                return_times += [elapsed_time]
                print(output)
                print("Search time: " + str(elapsed_time) + " seconds\n")

                # output time to results
            elif word != "zzend":
                print("Term not found in any documents")
        shutdown(return_times)
        g.close()
        h.close()
    else:
        print("Error opening file. Try again.")


def getcontext(string, wordnum):
    word_list = string.split()
    if len(word_list) < 11:
        return string[:-1]
    elif wordnum < 5:
        words = ' '.join(word_list[:10])
        return words
    elif wordnum > len(word_list)-10:
        words = ' '.join(word_list[-10:])
        return words
    else:
        words = ' '.join(word_list[wordnum-6:wordnum+4])
        return words


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
    test()
