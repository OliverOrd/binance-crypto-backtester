import config, csv
from binance.client import Client
import multiprocessing
import sys
import os

#timeframes = ["15", "30", "60", "120", "240", "360", "480", "720", "1440"]
timeframes = ["720", "1440"]


def get_data(timeframe, days_back):
    client = Client(config.API_KEY, config.API_SECRET)
    file = 'data/'
    file = file + timeframe + "_" + days_back + "d.csv"
    # print(file)

    klines = Client.KLINE_INTERVAL_15MINUTE
    days_back = days_back + " day ago UTC"
    # print(file, days_back)

    if timeframe == "15":
        klines = Client.KLINE_INTERVAL_15MINUTE
    elif timeframe == "30":
        klines = Client.KLINE_INTERVAL_30MINUTE
    elif timeframe == "60":
        klines = Client.KLINE_INTERVAL_1HOUR
    elif timeframe == "120":
        klines = Client.KLINE_INTERVAL_2HOUR
    elif timeframe == "240":
        klines = Client.KLINE_INTERVAL_4HOUR
    elif timeframe == "360":
        klines = Client.KLINE_INTERVAL_6HOUR
    elif timeframe == "480":
        klines = Client.KLINE_INTERVAL_8HOUR
    elif timeframe == "720":
        klines = Client.KLINE_INTERVAL_12HOUR
    elif timeframe == "1440":
        klines = Client.KLINE_INTERVAL_1DAY

    candles = client.get_historical_klines("BTCUSDT", klines, days_back)

    csvfile = open(file, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    for candlestick in candles:
        #print(candlestick)
        candlestick_writer.writerow(candlestick)

    print("timeframe:", timeframe, "# candles:", len(candles))


if __name__ == "__main__":

    directory = "data"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            os.remove(f)

    for timeframe in timeframes:
        p = multiprocessing.Process(target=get_data, kwargs={"timeframe": timeframe, "days_back": "10000"})
        p.start()