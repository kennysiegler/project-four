import csv
candlesticks = {}

    


with open('results/candlestick_data.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        createCandlestickDictionary(row)


print(candlesticks['2001']['dates'])


