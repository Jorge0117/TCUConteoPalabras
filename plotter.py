import matplotlib.pyplot as plt
import numpy as np
from math import log


class Plotter:

    def __init__(self, data, title, datasets=1):
        if datasets < 1:
            raise Exception('The number of data sets can\'t be less than 1')
        elif datasets == 1:
            self.data = [data]
        else:
            self.data = data
        self.title = title
        self.datasets = datasets

    # Data is a list of tuples
    def barPlot(self):
        data = self.addData()
        names = []
        values = []

        for value in data[:100]:
            names.append(value[0])
            values.append(value[1])

        '''
        for i in range(len(data)):
            names.append(log(i + 1, 10))
            values.append(log(data[i][1], 10))
        print(names)
        '''

        plt.rc('font', family='serif', size=8)
        plt.figure(figsize=(25, 6))
        plt.title = self.title
        plt.xlabel = 'Words'
        plt.ylabel = 'Number'
        plt.bar(names, values)
        plt.xticks(rotation=90)
        # plt.autoscale()
        # plt.show()
        plt.savefig('plots/' + self.title + '-bar.png')
        plt.close()

    def percentageBarPlot(self):
        data = self.addData()
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
        # plt.show()
        plt.savefig('plots/' + self.title + '-percentage.png')
        plt.close()

    # Adds the words from multiple documents.
    # Receive a list of dictionaries
    def addData(self):
        if self.datasets > 1:
            wordCount = {}
            for data in self.data:
                for key, value in data.items():
                    if key in wordCount:
                        wordCount[key] += value
                    else:
                        wordCount[key] = value
            return sorted(wordCount.items(), key=lambda kv: kv[1], reverse=True)
        else:
            return self.data[0]

    def generateTextFile(self):
        data = self.addData()
        file = open(self.title + '  SortedWordCount.txt', 'w', encoding="utf-8")
        for word in data:
            file.write(word[0] + ': ' + str(word[1]) + '\n')

    def scatterPlot(self):
        totalRank = []
        totalFrequency = []

        for i in range(self.datasets):
            rank = []
            frequency = []
            for index in range(len(self.data[i])):
                rank.append(log(index + 1, 10))
                frequency.append(log(self.data[i][index][1], 10))

            color = ""
            if i == 0: color = "b"
            elif i == 1: color = "g"
            elif i == 2: color = "r"
            elif i == 3: color = "c"
            elif i == 4: color = "m"
            elif i == 5: color = "y"
            elif i == 6: color = "k"
            elif i == 7: color = "w"
            # plotting points as a scatter plot
            plt.scatter(rank, frequency, label=i, color=color, s=30)
            totalFrequency += frequency
            totalRank += rank

        # Line of best fit
        plt.plot(np.unique(totalRank), np.poly1d(np.polyfit(totalRank, totalFrequency, 1))(np.unique(totalRank)))
        # x-axis label
        plt.xlabel('Rank')
        # frequency label
        plt.ylabel('Frequency')
        # plot title
        plt.title(self.title)
        plt.legend()
        # function to show the plot
        # plt.show()
        plt.savefig('plots/' + self.title + '.png')
        plt.close()
