from tika import parser


class PdfReader:
    documentName = ""
    document = None
    words = []
    wordCount = {}

    def __init__(self, documentName, blacklist, lowerCase, ignoreOneChar, removeSpecial):
        self.wordCount = {}
        self.documentName = documentName
        self.document = parser.from_file(documentName)
        if removeSpecial:
            curatedWords = self.document['content'].replace(',', ' ').replace('.', ' ').replace('(', ' ').replace(')', ' ') \
                .replace(';', ' ').replace(':', ' ').replace('/', ' ').replace('\\', ' ').replace('-', ' ').replace('[',
                                                                                                                    ' ') \
                .replace(']', ' ').replace('-', ' ').replace('*', ' ').replace('|', ' ').replace('’', ' ').replace('%', ' ') \
                .replace('~', ' ').replace('&', ' ')
        else:
            curatedWords = self.document['content']

        curatedWords = ''.join([i for i in curatedWords if not i.isdigit()])
        self.words = curatedWords.split()
        for word in self.words:
            if ignoreOneChar and len(word) == 1:
                continue
            if lowerCase:
                word = word.lower()
            if word in blacklist:
                self.words.remove(word)
            else:
                if word in self.wordCount:
                    self.wordCount[word] += 1
                else:
                    self.wordCount[word] = 1

    def getName(self):
        return self.documentName[self.documentName.rfind('/') + 1:]

    def getWords(self):
        return self.words

    def getWordCount(self):
        return self.wordCount

    def getSortedWordCount(self):
        return sorted(self.wordCount.items(), key=lambda kv: kv[1], reverse=True)

    def sortWordCount(self, wordCount):
        return sorted(wordCount.items(), key=lambda kv: kv[1], reverse=True)

