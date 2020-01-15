import ntpath
import os
from appJar import gui

from pdfReader import PdfReader
from plotter import Plotter


class WordCountPlotter:

    def __init__(self):
        self.groupCount = 0
        app = gui()

        self.options = {
            'fileExtension': '.pdf',
            'scatter': True,
            'bar': True,
            'barPercentage': True,
            'lowercase': True,
            'ignoreOneWord': True,
            'removeSpecial': True,
            'groupGraphs': True,
            'textFile': False
        }

        app.setSize(800, 600)
        app.setIcon('icons8-document-50.gif')
        app.setResizable(canResize=False)
        app.setTitle("Word count plotter")
        app.addLabel('title', 'Word Count Plotter')
        app.addButton('Blacklist words', self.OpenWordBlacklist)
        app.addButton('Options', self.OpenOptions)
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

        app.stopSubWindow()

        app.startSubWindow("Options", modal=True)
        app.setSize(630, 300)
        app.setResizable(canResize=False)
        app.setLocation('center')

        app.setExpand("both")
        app.addLabel("opTitle", "Options", 0, 0, 3)
        app.setSticky('w')
        app.addLabel("output", "Output file extension", 1, 0)
        app.addRadioButton("outputType", ".pdf", 2, 0)
        app.addRadioButton("outputType", ".png", 2, 1)
        app.addLabel("graphTypes", "Output graphs", 3, 0)
        app.addCheckBox("Scatter", 4, 0)
        app.addCheckBox("Bar (Word count)", 4, 1)
        app.addCheckBox("Bar (Word percentage)", 4, 2)
        app.addLabel("Options", "Options", 5, 0)
        app.addCheckBox("Lower case", 6, 0)
        app.addCheckBox("Ignore one character words", 6, 1)
        app.addCheckBox("Remove special characters", 6, 2)
        app.addCheckBox("Generate group graphs", 7, 0)
        app.addCheckBox("Generate text file", 7, 1)

        app.setSticky('')
        app.addButton("Save", self.SaveOptions, 8, 0, 3)

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
        files = self.app.openBox(multiple=True, fileTypes=[('document', '*.pdf')])
        if len(files) > 0:
            index = int(btn[5:])
            text = ''

            for i in range(len(files)):
                filename, fileExtension = os.path.splitext(files[i])
                if fileExtension != '.pdf':
                    self.app.errorBox('File type not accepted', 'The type of the selected file is not accepted. '
                                                                'Every file has to be a pdf.')
                    return

                text += files[i]
                if i < len(files) - 1:
                    text += '\n'

            self.files[index] = files
            self.app.setMessage("Selected Files " + str(index), text)

    def OpenOptions(self):
        self.app.setRadioButton('outputType', self.options['fileExtension'])
        self.app.setCheckBox('Scatter', self.options['scatter'])
        self.app.setCheckBox('Bar (Word count)', self.options['bar'])
        self.app.setCheckBox('Bar (Word percentage)', self.options['barPercentage'])
        self.app.setCheckBox('Lower case', self.options['lowercase'])
        self.app.setCheckBox('Ignore one character words', self.options['ignoreOneWord'])
        self.app.setCheckBox('Remove special characters', self.options['removeSpecial'])
        self.app.setCheckBox('Generate group graphs', self.options['groupGraphs'])
        self.app.setCheckBox('Generate text file', self.options['textFile'])
        self.app.showSubWindow('Options')

    def SaveOptions(self):
        self.options['fileExtension'] = self.app.getRadioButton('outputType')
        self.options['scatter'] = self.app.getCheckBox('Scatter')
        self.options['bar'] = self.app.getCheckBox('Bar (Word count)')
        self.options['barPercentage'] = self.app.getCheckBox('Bar (Word percentage)')
        self.options['lowercase'] = self.app.getCheckBox('Lower case')
        self.options['ignoreOneWord'] = self.app.getCheckBox('Ignore one character words')
        self.options['removeSpecial'] = self.app.getCheckBox('Remove special characters')
        self.options['groupGraphs'] = self.app.getCheckBox('Generate group graphs')
        self.options['textFile'] = self.app.getCheckBox('Generate text file')
        self.app.hideSubWindow('Options')

    def OpenWordBlacklist(self):
        self.app.showSubWindow('Blacklisted Words')

    def AddBLWord(self):
        word = self.app.stringBox('Blacklist Word', 'Write the word you would like to blacklist',
                                  parent='Blacklisted Words')
        if word is not None and word is not '':
            self.app.addListItem('blacklistedWords', word)

    def RemoveBLWord(self):
        word = self.app.getListBox('blacklistedWords')
        if len(word) > 0:
            self.app.removeListItem('blacklistedWords', word)

    def ClearBlWords(self):
        self.app.clearListBox('blacklistedWords')

    def OpenBLFile(self):
        try:
            fileDir = self.app.openBox(fileTypes=[('text', '*.txt')], parent='Blacklisted Words')
            filename, fileExtension = os.path.splitext(fileDir)

            if fileDir is not None:
                if fileExtension != '.txt':
                    self.app.errorBox('Error', 'The type of the selected file is not accepted. '
                                               'Every file has to be a txt.')
                    return

                file = open(fileDir, 'r', encoding='utf-8')
                words = file.read().split('\n')
                for word in words:
                    if word is not '':
                        self.app.addListItem('blacklistedWords', word)
        except Exception as e:
            self.app.errorBox('Error', 'An error occurred while opening the file. Make sure the format is correct.')
            print(e)

    def SaveBLFile(self):
        try:
            words = self.app.getAllListItems('blacklistedWords')
            saveDir = self.app.saveBox('Save Location', 'blacklisted_words', fileExt=".txt", parent='Blacklisted Words')
            if saveDir is not None:
                file = open(saveDir, 'w', encoding="utf-8")
                for word in words:
                    file.write(word + '\n')
                file.close()
        except:
            self.app.errorBox('Error', 'An error occurred while saving the file.')

    def Generate(self):
        if len(self.files) == 0:
            self.app.errorBox('Error', 'Please add at least one group.')
            return

        for i in range(len(self.files)):
            if self.app.getEntry('Group ' + str(i) + ' name') == '':
                self.app.errorBox('Error', 'Every group has to be named.')
                return

            if len(self.files[i]) == 0:
                self.app.errorBox('Error', 'Every group has to have at least one file.')
                return

        saveDir = self.app.directoryBox()
        if saveDir == '':
            return

        blacklist = self.app.getAllListItems('blacklistedWords')
        try:
            for i in range(len(self.files)):
                data = []
                names = []
                for j in range(len(self.files[i])):
                    filename = ntpath.basename(self.files[i][j])
                    pdf = PdfReader(self.files[i][j], blacklist, self.options['lowercase'], self.options['ignoreOneWord'], self.options['removeSpecial'])
                    fileData = pdf.getSortedWordCount()
                    data.append(fileData)
                    names.append(filename)

                    plotter = Plotter(fileData, filename, [filename],
                                      saveDir + '/' + self.app.getEntry('Group ' + str(i) + ' name'))
                    if self.options['bar']:
                        plotter.barPlot(self.options['fileExtension'])

                    if self.options['barPercentage']:
                        plotter.percentageBarPlot(self.options['fileExtension'])

                    if self.options['scatter']:
                        plotter.scatterPlot(self.options['fileExtension'])

                    if self.options['textFile']:
                        plotter.generateTextFile()

                if len(data) > 1 and self.options['groupGraphs']:
                    plotter = Plotter(data, self.app.getEntry('Group ' + str(i) + ' name'), names,
                                      saveDir + '/' + self.app.getEntry('Group ' + str(i) + ' name'), len(data))
                    plotter.barPlot(self.options['fileExtension'])
                    plotter.percentageBarPlot(self.options['fileExtension'])
                    plotter.scatterPlot(self.options['fileExtension'])
        except Exception as e:
            self.app.errorBox('Error', 'An error has occurred while generating the plots. Please try again.\n' + str(e))

        return


app = WordCountPlotter()
app.Start()
