import ntpath
import os
from appJar import gui

from pdfReader import PdfReader
from plotter import Plotter


class WordCountPlotter():

    def __init__(self):
        self.groupCount = 0
        app = gui()
        app.setSize(800, 600)
        app.setResizable(canResize=False)
        app.setTitle("Word count plotter")
        app.addLabel('title', 'Word Count Plotter')
        app.addButton('Blacklist words', self.OpenWordBlacklist)
        app.addButton('Add Group', self.AddGroup)
        app.startScrollPane('groups')
        app.stopScrollPane()
        app.setScrollPaneWidth('groups', 100)
        app.addButton('Generate', self.Generate)

        app.startSubWindow('Blacklisted Words', modal=True)
        app.setSize(600, 500)
        app.setResizable(canResize=False)
        app.setLocation('center')

        app.setSticky("news")
        app.setExpand("both")
        app.addLabel("blTitle", "Blacklisted words", 0, 0, 3)
        app.addListBox("blacklistedWords", [], 1, 0, 2, 5)
        app.addButton('Add Word', self.AddBLWord, 1, 2)
        app.addButton('Remove Word', self.RemoveBLWord, 2, 2)
        app.addButton('Clear Words', self.ClearBlWords, 3, 2)
        app.addButton('Load File', self.OpenBLFile, 4, 2)
        app.addButton('Save File', self.SaveBLFile, 5, 2)

        app.addLabel("l9", "row=3\ncolumn=1", 6, 1)



        app.stopSubWindow()

        self.app = app
        self.files = []

    def Start(self):
        self.app.go()

    def AddGroup(self):
        self.app.openScrollPane('groups')
        self.app.startLabelFrame('Group ' + str(self.groupCount))
        self.app.addLabelEntry('Group ' + str(self.groupCount) + ' name')
        self.app.setEntryWidth('Group ' + str(self.groupCount) + ' name', 72)
        self.app.addMessage("Selected Files " + str(self.groupCount), """No files selected""")
        self.app.setMessageWidth("Selected Files " + str(self.groupCount), 900)
        self.app.addNamedButton('Select files', 'files' + str(self.groupCount), self.SelectFiles)
        self.app.stopLabelFrame()
        self.groupCount += 1
        self.files.append([])
        self.app.stopScrollPane()

    def SelectFiles(self, btn):
        files = self.app.openBox(multiple=True)
        index = int(btn[5:])
        text = ''
        self.files[index] = files

        if len(self.files[index]) == 0:
            self.app.setMessage("Selected Files " + str(index), """No files selected""")
        else:
            for i in range(len(self.files[index])):
                text += self.files[index][i]
                if i < len(self.files[index]) - 1:
                    text += '\n'

        self.app.setMessage("Selected Files " + str(index), text)

    def OpenWordBlacklist(self):
        self.app.showSubWindow('Blacklisted Words')

    def AddBLWord(self):
        word = self.app.stringBox('Blacklist Word', 'Write the word you would like to blacklist', parent='Blacklisted Words')
        if word is not None and word is not '':
            self.app.addListItem('blacklistedWords', word)

    def RemoveBLWord(self):
        word = self.app.getListBox('blacklistedWords')
        if len(word) > 0:
            self.app.removeListItem('blacklistedWords', word)

    def ClearBlWords(self):
        self.app.clearListBox('blacklistedWords')

    def OpenBLFile(self):
        fileDir = self.app.openBox(fileTypes=[('text', '*.txt')], parent='Blacklisted Words')
        if fileDir is not None:
            file = open(fileDir, 'r')
            words = file.read().split('\n')
            for word in words:
                if word is not '':
                    self.app.addListItem('blacklistedWords', word)

    def SaveBLFile(self):
        words = self.app.getAllListItems('blacklistedWords')
        saveDir = self.app.saveBox('Save Location', 'blacklisted_words', fileExt=".txt", parent='Blacklisted Words')
        if saveDir is not None:
            file = open(saveDir, 'w', encoding="utf-8")
            for word in words:
                file.write(word + '\n')
            file.close()

    def ConfirmBL(self):
        pass

    def Generate(self):
        saveDir = self.app.directoryBox()
        blacklist = self.app.getAllListItems('blacklistedWords')
        for i in range(len(self.files)):
            data = []
            names = []
            for j in range(len(self.files[i])):
                filename = ntpath.basename(self.files[i][j])
                pdf = PdfReader(self.files[i][j], blacklist)
                fileData = pdf.getSortedWordCount()
                data.append(fileData)
                names.append(filename)

                plotter = Plotter(fileData, filename, [filename],
                                  saveDir + '/' + self.app.getEntry('Group ' + str(i) + ' name'))
                plotter.barPlot()
                plotter.percentageBarPlot()
                plotter.scatterPlot()

            if len(data) > 1:
                plotter = Plotter(data, self.app.getEntry('Group ' + str(i) + ' name'), names,
                                  saveDir + '/' + self.app.getEntry('Group ' + str(i) + ' name'), len(data))
                plotter.barPlot()
                plotter.percentageBarPlot()
                plotter.scatterPlot()


app = WordCountPlotter()
app.Start()
'''
pdf = PdfReader('Converging science and literature cultures_OAHS.pdf')
data = pdf.getSortedWordCount()
plotter.generateTextFile(data, pdf.getName())
plotter.barPlot(data, pdf.getName())
plotter.percentageBarPlot(data)

pdf2 = PdfReader('Random texts do not exhibit the real Zipfs law-like rank distribution.pdf')
data2 = pdf2.getSortedWordCount()
plotter.generateTextFile(data2, pdf2.getName())
plotter.barPlot(data2, pdf.getName())
plotter.percentageBarPlot(data2)

combinedData = plotter.addData([pdf.getWordCount(), pdf2.getWordCount()])
plotter.barPlot(combinedData, 'combined')
plotter.percentageBarPlot(combinedData)
plotter.generateTextFile(combinedData, 'Combined data')
'''
'''
pdf = PdfReader('documents/Bibliometry of marine science and limnology publications.pdf')
data = pdf.getSortedWordCount()
pdf2 = PdfReader('documents/Evaluation of Microleakage.pdf')
data2 = pdf2.getSortedWordCount()
plotter = Plotter([data, data2], 'two test', 2)
plotter.scatterPlot()
'''
'''
data = []
names = []
for doc in os.listdir('documents'):

    pdf = PdfReader('documents/' + doc)
    data.append(pdf.getSortedWordCount())
    names.append(doc)

plotter = Plotter(data, 'Primer grupo', names, len(data))
plotter.scatterPlot()

plotter.barPlot()
plotter.percentageBarPlot()
'''
