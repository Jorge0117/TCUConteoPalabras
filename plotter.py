import matplotlib.pyplot as plt

class Plotter:

    # Data is a list of tuples
    def barPlot(self, data, title):
        names = []
        values = []

        for value in data[:100]:
            names.append(value[0])
            values.append(value[1])

        plt.rc('font', family='serif', size=8)
        plt.figure(figsize=(25, 6))
        plt.title = title
        plt.xlabel = 'Words'
        plt.ylabel = 'Number'
        plt.bar(names, values)
        plt.xticks(rotation=90)
        #plt.autoscale()
        plt.show()

    def percentageBarPlot(self, data):
        names = []
        values = []
        total = 0

        for value in data[:100]:
            names.append(value[0])
            values.append(value[1])
            total += value[1]

        for i in range(len(values)):
            values[i] = values[i] / total * 100

        plt.rc('font', family='serif', size=8)
        plt.figure(figsize=(25, 6))
        plt.xlabel = 'Words'
        plt.ylabel = 'Number'
        plt.bar(names, values)
        plt.xticks(rotation=90)
        # plt.autoscale()
        plt.show()

    # Adds the words from multiple documents.
    # Receive a list of dictionaries
    def addData(self, datasets):
        wordCount = {}
        for data in datasets:
            for key, value in data.items():
                if key in wordCount:
                    wordCount[key] += value
                else:
                    wordCount[key] = value
        return sorted(wordCount.items(), key=lambda kv: kv[1], reverse=True)

    def generateTextFile(self, data, documentName):
        file = open(documentName + '  SortedWordCount.txt', 'w', encoding="utf-8")
        for word in data:
            file.write(word[0] + ': ' + str(word[1]) + '\n')