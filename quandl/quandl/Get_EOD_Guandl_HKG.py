from datetime import date, timedelta
import quandl
import os
import pandas as pd 

#Get todays date in Y-m-d format to use in the Guandl API call
dateEnd = date.today().strftime("%Y-%m-%d")

#Get start date in Y-m-d format to use in the Guandl API call to download 1 year data. You can change the number to get 3, 5 or 10 years data
startDate = date.today() + timedelta(-365)
dateStart=startDate.strftime("%Y-%m-%d")

#Set the folder for storing the downloaded data
#dataPath='D:/Temp/Data/GuandlEOD'

dataPath_1YD='./data'

#Guandl API Key
quandl.ApiConfig.api_key = 'uKq9y5JVXcGiBXTdPDsN'

#Exchange
exchange = 'HKEX'

#If no such folder exists, create an empty folder
if not os.path.exists(dataPath_1YD):
    os.makedirs(dataPath_1YD)
    print ('creating Directory ...' + dataPath_1YD)


#Get 1Y EOD from Guandl
def GuandlDailyDatatoCSV(symbol):
    """
    This function will download EOD data from Guandl
    and write to a csv file called nameOfSymbol.csv
    """

    #symbol='0005'
    #symbolFile=os.path.join(dataPath, symbol[1:]+".HK.csv")

    print('donwloading ', symbol, '...')

    try:
        # get price data (return pandas dataframe)
        dff = quandl.get('{0}/{1}'.format(exchange, symbol), start_date=dateStart, end_date=dateEnd)
        dff['Open'] = dff['Previous Close']
        dff['Close'] = dff['Nominal Price']
        dff['Volume'] = dff['Share Volume (000)'].astype('int') * 1000
        #dff['Turnover'] = dff['Turnover (000)']
        df = dff[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
        #print(df.tail(5))

        # save the data to csv in the specified folder and file name
        symbolFile_1YD=os.path.join(dataPath_1YD, symbol[1:]+".HK.csv")
        #df.to_csv(symbolFile_1YD, header=False)
        df.to_csv(symbolFile_1YD, header=True)

        #df['Date'] = df.index.astype(str)
        #df['Date'], df['Time'] = df['Date'].str.split(' ' ,1).str
        #df.to_csv(symbolFile, header=True)

        print('finished writing ', symbol, 'csv file.')

    except Exception as e:
        print('error downloading {0}: {1}'.format(symbol, str(e)))



########################################
#--------------------START -------------
print ('Delete all .csv files in ' + dataPath_1YD)

# remove all files in the existing folder
#for file in os.listdir(dataPath):
#       if file[-3:].lower() == 'csv':
#           os.remove(dataPath + "\\" + file)

# remove all files in the existing folder
for file in os.listdir(dataPath_1YD):
       if file[-3:].lower() == 'csv':
           os.remove(dataPath_1YD + '/' + file)


#filePath = 'D:/Python_Project/HKEX_Ticker.xlsx'
filePath = './HKEX_Ticker.xlsx'
dfHKG = pd.read_excel(filePath, sheet_name='HKEX_Ticker')

##---------------Download all tickers and write to csv       
for i in range(0, len(dfHKG)):
    ticker = dfHKG.iloc[i]['Ticker']
    ticker=ticker.replace('.HK', '')
    ticker='{:0>5}'.format(ticker)
    GuandlDailyDatatoCSV(ticker)
