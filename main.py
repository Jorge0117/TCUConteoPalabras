'''
from appJar import gui

app = gui()
app.setSize(1024, 576)

app.go()
'''
from pdfReader import PdfReader
from plotter import Plotter
plotter = Plotter()

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