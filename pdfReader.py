from tika import parser


class PdfReader:
    documentName = ""
    document = None
    words = []
    wordCount = {}

    def __init__(self, documentName, blacklist, lowerCase, ignoreOneChar, oneCharExceptions, removeSpecial, removeList):
        self.wordCount = {}
        self.documentName = documentName
        self.document = parser.from_file(documentName)
        curatedWords = self.document['content']
        if removeSpecial:
            for char in removeList:
                curatedWords = curatedWords.replace(char, ' ')

        curatedWords = ''.join([i for i in curatedWords if not i.isdigit()])
        self.words = curatedWords.split()
        for word in self.words:
            if lowerCase:
                word = word.lower()
            if ignoreOneChar and len(word) == 1:
                if word not in oneCharExceptions:
                    continue
            if word in blacklist and word in self.words:
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
