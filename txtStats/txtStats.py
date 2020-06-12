# Author: Ansh Chandnani
# May 13, 2020
# Python program to find Term Frequencies and Dictionary Frequencies for a given set of text files

class Document:
    def __init__(self, doc_id):                 # parameterized constructor
        self.id = doc_id
        self.wordlist = {}                      # dictionary {key1: value1, key2: value2 .....}

    def tokenize(self, text):
        text = text.replace(',', ' ').replace('.', ' ').replace('?', ' ').replace('!', ' ')
        textList = text.split(' ')
        for word in textList:
            word = word.lower()
            if word in self.wordlist:           # code case if word is present in the dictionary
                self.wordlist[word] += 1
            else:                               # code case if word is not present in the dictionary
                self.wordlist.update({word: 1})


def save_dictionary(dict_data, file_path_name):
    savedFile = open(file_path_name, 'w+')      # opening file in write mode, creates new file if needed
    for i in dict_data:
        savedFile.write("%s %s \t" % (i, dict_data[i]))


def vectorize(data_path):
    DFstats = {}
    for i in range(1, 21):
        fileName = str(data_path) + str(i) + '.txt'
        file = open(fileName, 'r')
        content = file.read()
        # Creating object - wordlist, functions
        docs = Document(i)
        docs.tokenize(content)              # dictionary created in docs.wordlist
        # Contributing to DFstats
        content = content.replace(',', ' ').replace('.', ' ').replace('?', ' ').replace('!', ' ')
        contentList = content.split(' ')
        for word in contentList:
            word = word.lower()
            if word in DFstats:
                DFstats[word] += 1
            else:
                DFstats.update({word: 1})
        # Saving TF to individual files
        savePath = 'tf_' + str(docs.id) + '.txt'
        save_dictionary(docs.wordlist, savePath)
    # Saving DFstats to external file
    save_dictionary(DFstats, 'df.txt')


vectorize('./')                             # performs operation in current directory (./)
