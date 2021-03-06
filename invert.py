import re
from porter import PorterStemmer


def create_index():
    # ask if stop word removal
    # ask if stemming
    use_stop_word = False
    stop_words = []
    use_stem = False

    txt1 = input("Do you want to use stop word removal? [Y/N]")
    txt2 = input("Do you want to use stemming? [Y/N]")
    if txt1 == "Y" or txt1 == "Yes" or txt1 == "yes" or txt1 == "y":
        use_stop_word = True
        stop_words = open("stopwords.txt", "r").read().split('\n')

    if txt2 == "Y" or txt2 == "Yes" or txt2 == "yes" or txt2 == "y":
        use_stem = True

    term_dict = dict()
    document_num = 0
    document_pos = 0
    start_scan = False

    f = open("cacm.all", "r")
    if f.mode == 'r':
        lines = f.readlines()
        for line in lines:
            if line.startswith("."):
                start_scan = False
            if line.startswith(".I"):
                document_num += 1
                document_pos = 0
            if start_scan is True:
                line = re.sub('[\-]+', ' ', line)
                line = re.sub('(?<=[,])(?=[^\s])(?=[A-Z])', ' ', line)
                words = str.split(line)
                for word in words:
                    document_pos += 1
                    # words are made lower case right from the start
                    word = word.lower()
                    word = re.sub('[^A-Za-z0-9$]+', '', word)
                    if use_stem:
                        word = stem(word)
                    if use_stop_word:
                        if not word in stop_words:
                            fill_dict(word, term_dict, document_num, document_pos)
                    else:
                        if word != '':
                            fill_dict(word, term_dict, document_num, document_pos)
            if line.startswith(".T") or line.startswith(".W") or line.startswith(".A"):
                start_scan = True
    print_dict(term_dict, use_stem, use_stop_word)


def fill_dict(word, term_dict, document_num, document_pos):
    if word in term_dict:
        # check to see if there is an entry for the current document
        # for that I need to check the first element of the last list in the list of lists
        # in the value of the dict
        if term_dict[word][-1][0] == document_num:
            term_dict[word][-1][1] += 1
            term_dict[word][-1][2] += [document_pos]
        else:
            term_dict[word].append([document_num, 1, [document_pos]])
    else:
        term_dict[word] = [[document_num, 1, [document_pos]]]


def print_dict(term_dict, use_stem, use_stop):
    g = open("postings.txt", "w")
    if use_stem:
        g.write("1")
    else:
        g.write("0")
    if use_stop:
        g.write("1\n")
    else:
        g.write("0\n")
    for key, value in sorted(term_dict.items()):
        g.write('["' + key + '", ' + str(value) + "],\n")
    g.close()


def stem(word):
    p = PorterStemmer()
    return p.stem(word, 0, len(word) - 1)


if __name__ == "__main__":
    create_index()
