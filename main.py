import os
'''
from appJar import gui

app = gui()
app.setSize(1024, 576)

app.go()
'''
from pdfReader import PdfReader
from plotter import Plotter

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
data = []
names = []
for doc in os.listdir('documents'):

    pdf = PdfReader('documents/' + doc)
    data.append(pdf.getSortedWordCount())
    names.append(doc)

plotter = Plotter(data, 'Primer grupo', names, len(data))
plotter.scatterPlot()

#plotter.barPlot()
#plotter.percentageBarPlot()