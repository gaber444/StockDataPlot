from typing import List,Union
import csv
import numpy as np
import os
import yfinance as yahooFinance
import yahoo_fin.stock_info as si
import matplotlib.pyplot as plt


class PlotStocksPrices():
    #class constants
    AVE_FIVE = 5
    AVE_TEN = 10
    AVE_TWENTY = 20

    def __init__(self,tickerOrTickers: Union[str,List[str]]):
        if isinstance(tickerOrTickers,str):
            if tickerOrTickers.strip() == "": # Check if string is empty.
                raise ValueError("Input string cannot be empty !")
            self._tickerOrTickersSymbol = [tickerOrTickers.upper()]
        elif isinstance(tickerOrTickers,list):# Check if the list is empty
            if not tickerOrTickers:
                raise ValueError("Input list cannot be empty !")
            else:
                filter_list = [item.strip().upper() for item in tickerOrTickers if isinstance(item,str) and item.strip() != ""]
                self._tickerOrTickersSymbol = filter_list
        
        self._date = []
        self._openPrice = []
        self._highPrice = []
        self._lowPrice = []
        self._closePrice = []
        self._volume = []
        self._stockPriceVolume = []
        self._averageFiveClosedPrices = []
        self._averageFiveVolumes = []
        self._averageFiveLowPrice = []
        self._stockPriceAverageFiveVolumes = []
        self._legendForDates = {}
        self._closePricesLabeled = {}

        #data
        self._maxStockClosePrice = 0.0
        self._maxVolume = 0.0
        self._average20 = []
        self._average10 = []
        self._averageOverAllData = 0 # averageOneYear
        self._sumOverAlldata = 0.0 #sumOneYear
        self._x = 0
        self._x10 = 0
        self._x20 = 0

    #variables:
    def reset(self):
        self._date = []
        self._openPrice = []
        self._highPrice = []
        self._lowPrice = []
        self._closePrice = []
        self._volume = []
        self._stockPriceVolume = []
        self._averageFiveClosedPrices = []
        self._averageFiveVolumes = []
        self._averageFiveLowPrice = []
        self._stockPriceAverageFiveVolumes = []
        self._legendForDates = {}
        self._closePricesLabeled = {}

        #data
        self._maxStockClosePrice = 0.0
        self._maxVolume = 0.0
        self._average20 = []
        self._average10 = []
        self._averageOverAllData = 0 # averageOneYear
        self._sumOverAlldata = 0.0 #sumOneYear
        self._x = 0
        self._x10 = 0
        self._x20 = 0


    def getCurrentDirectory(self):
        return os.getcwd()

    def SetStartEndDate(self,startDate:str,endDate:str):
        self._startDate = startDate
        self._endDate = endDate
        
    def display_all_ticker_Symbols(self):
        for i in self.tickerOrTickers:
            print(i)

    def downloadDataFromYAHOO(self,tickerOrTickers: List[str]):
        output_dir = self.getCurrentDirectory() + "/STOCKDATA/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for ticker in tickerOrTickers:
             data = yahooFinance.download(ticker,self._startDate,self._endDate)
             data.to_csv(output_dir + ticker+ ".csv")

    def setMaxStockClosePrice(self):
        self._maxStockClosePrice = float("{:.2f}".format(max(self._closePrice)))

    def getMaxStockClosePrice(self):
        return self._maxStockClosePrice
    
    def setMaxStockVolume(self):
        self._maxVolume = max(self._volume)
    
    def getMaxStockVolume(self):
        return self._maxVolume
    
    def averageOfFiveDays(self):
        start: int = 0
        stop: int = 5
        sum: float = 0.0
        average : float = 0.0
        sumAverageLowPrice: float = 0.0

        while stop <= len(self._closePrice):
            for i in range(start,stop):
                self._legendForDates[self._date[stop - 1]] = start + 1
                self._closePricesLabeled[self._closePrice[stop - 1]] = start + 1
                sum = sum + self._closePrice[i]
                average = average + self._volume[i]
                sumAverageLowPrice = sumAverageLowPrice + self._lowPrice[i]

            self._averageFiveClosedPrices.append(float("{:.2f}".format(sum/PlotStocksPrices.AVE_FIVE)))
            self._averageFiveVolumes.append(average/PlotStocksPrices.AVE_FIVE)
            self._averageFiveLowPrice.append(float("{:.2f}".format(sumAverageLowPrice/PlotStocksPrices.AVE_FIVE)))

            sum = 0
            average = 0
            sumAverageLowPrice = 0
            start += 1
            stop += 1
    
    def averageOfLast20Days(self):
        begin: int = 0
        end: int  = 20
        sum20days: float = 0.0

        while end <= len(self._closePrice):
            for h in range(begin,end):
                sum20days = sum20days + self._closePrice[h]
            self._average20.append(float("{:.2f}".format(sum20days/PlotStocksPrices.AVE_TWENTY)))
            sum20days = 0
            begin +=1
            end +=1

    def averageOfLast10Days(self):
        begin: int = 0
        end: int = 10
        sum10days: float = 0.0

        while end <= len(self._closePrice):
            for h in range(begin,end):
                sum10days = sum10days + self._closePrice[h]
            self._average10.append(float("{:.2f}".format(sum10days/PlotStocksPrices.AVE_TEN)))
            sum10days = 0
            begin +=1
            end +=1

    def averageOverAllData(self):
        for i in self._closePrice:
            self._sumOverAlldata += i
        self._averageOverAllData = self._sumOverAlldata / len(self._closePrice)

    def setXlabels(self):
        self._x = np.linspace(start = 1, stop = len(self._averageFiveClosedPrices), num = len(self._averageFiveClosedPrices))
        self._x10 =  np.linspace(start = 9, stop = len(self._averageFiveClosedPrices), num = len(self._average10))
        self._x20 = np.linspace(start = 19, stop = len(self._averageFiveClosedPrices), num = len(self._average20))

    def normalizeVolume(self):
        for j in range(len(self._averageFiveVolumes)):
            self._stockPriceAverageFiveVolumes.append(float("{:.2f}".format((self.getMaxStockClosePrice() * self._averageFiveVolumes[j]) / self.getMaxStockVolume())))
            self._stockPriceVolume.append(float("{:.2f}".format((self.getMaxStockClosePrice() * self._volume[j + 4]) / self.getMaxStockVolume())))

    def plotStockPricesWithNoromalizeVolume(self,tickerSymbol:str):
        plt.figure()
        plt.title(tickerSymbol + ' NORMALIZED WITH STOCK PRICE')
        plt.plot(self._x,self._averageFiveClosedPrices,color = 'blue',label ='AVERAGE CLOSE PRICE')
        plt.plot(self._x,self._closePrice[4:],color = 'black',label = 'CLOSE PRICE')
        plt.plot(self._x,self._stockPriceAverageFiveVolumes,color = 'red',label ='AVERAGE VOLUMES')
        plt.bar(self._x,self._stockPriceVolume,color = 'green',label = 'VOLUMES')
        plt.xlabel('day')
        plt.ylabel('stock price')
        plt.legend()
        plt.show()  

    def plotStockPrize(self,tickerSymbol:str):
        plt.figure()
        plt.title(tickerSymbol)
        plt.plot(self._x,self._averageFiveClosedPrices,color = 'blue',label ='AVERAGE CLOSE PRICE')
        plt.plot(self._x,self._closePrice[4:],color = 'black',label = 'CLOSE PRICE')
        plt.plot(self._x10,self._average10,color = "magenta",label="AVERAGE LAST 10 DAYS")
        plt.plot(self._x20,self._average20,color = "orange",label="AVERAGE LAST 20 DAYS")
        plt.hlines(y=self._averageOverAllData,xmin = self._x[0], xmax = self._x[-1],label = f'{len(self._x)} DAYS AVERAGE')
        plt.hlines(y=(0.8*self._averageOverAllData),xmin = self._x[0], xmax = self._x[-1],color= 'green',label = 'BUY ZONE')
        plt.xlabel('day')
        plt.ylabel('stock price')
        plt.legend()
        plt.show()

    def showPredictions(self):
        for tickerSimbol in self._tickerOrTickersSymbol:
            with open('STOCKDATA/' + tickerSimbol + '.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self._date.append(row['Date'])
                    self._openPrice.append(float(row['Open']))
                    self._highPrice.append(float(row['High']))
                    self._lowPrice.append(float(row['Low']))
                    self._closePrice.append(float(row['Close']))
                    self._volume.append(int(row['Volume']))
            
            self.setMaxStockClosePrice()
            self.setMaxStockVolume()
            self.averageOfFiveDays()
            self.averageOfLast10Days()
            self.averageOfLast20Days()
            self.averageOverAllData()
            self.setXlabels()
            self.normalizeVolume()
            self.plotStockPrize(tickerSimbol)
            self.plotStockPricesWithNoromalizeVolume(tickerSimbol)
            self.reset()

    def combineAll(self):
        self.downloadDataFromYAHOO(self._tickerOrTickersSymbol)
        self.showPredictions()

def main():
    #example
    start_date: str = '2023-05-21'
    end_date: str = '2024-05-21'

    tickers: list = ['AAPL','MU']

    m_stock = PlotStocksPrices(tickers)
    m_stock.SetStartEndDate(start_date,end_date)
    m_stock.combineAll()


if __name__ == '__main__':
    main()