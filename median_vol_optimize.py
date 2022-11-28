import csv
import numpy as np
import math
from numpy import genfromtxt
import datetime
import sys
import os
import multiprocessing

# Median Volatility
def median_volatility(source, period: int):
    sqrt_annual = math.sqrt(365) * 100

    median = np.median(source)
    E = 0.0
    for i in range(period):
        E = E + abs(source[i] - median)

    return sqrt_annual * math.sqrt(2) * (E / period)

def optimize(start, end, step, lookback, f):
    fee_level = 0.005
    # fee_level = 0.0
    # print(f)
    data = genfromtxt(f, delimiter=',')
    print(f.replace("data/", ""), " NEW OPTIMIZATION RUN!! Start: ", start, " End: ", end, " Step: ", step,
          " Lookback: ", lookback,
          sep="")

    highest_return = -101.0
    optimal_period = 0.0
    optimal_buy_hold = 0.0
    optimal_drawdown = 0.0

    test_period = start

    timestamp = np.copy(data[:, 0])
    openp = np.copy(data[:, 1])
    close = np.copy(data[:, 4])

    timestamp = timestamp[:-1]
    #openp = openp[:-1]
    close = close[:-1]

    logr = np.diff(np.log(np.array(close, dtype=np.float64)))
    timestamp = timestamp[1:]
    close = close[1:]
    openp = openp[1:]
    upR = np.copy(logr)
    downR = np.copy(logr)
    for i in range(len(upR)):
        if upR[i] < 0:
            upR[i] = 0
        if downR[i] > 0:
            downR[i] = 0

    z = []

    results_file = f.replace(".csv", "")
    results_file = results_file.replace("data", "results")
    results_file += "_" + str(lookback)
    results_file += "_results.csv"

    csvfile = open(results_file, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    while test_period < end:

        bought = False
        profits = []
        starting_balance = 100000
        balance = 100000
        min_balance = 100000
        max_balance = 100000
        position = 0
        trade_count = 0
        account = []
        initial_buy = 0
        end_buy = 0
        lookback = test_period

        for i in range(lookback,len(close)+1):
            if len(upR[i - lookback: i]) > 1:
                upSRC = median_volatility(upR[i - lookback: i], test_period)
                downSRC = median_volatility(downR[i - lookback: i], test_period)
                momentum = np.subtract(upSRC, downSRC)
                #print(momentum, logr[i - lookback: i], openp[i], i, lookback)
                z.append(momentum)
                # print(z[-1], openp[i], i)

                if len(z) > 1:
                    if z[-1] > 0 and bought == False:
                        start_price = openp[i]
                        balance = balance * (1 - (fee_level / 100))
                        # print(round(z[-1],2), " Bought @ ", start_price, " ", i, sep="")
                        position = balance / start_price
                        bought = True
                        if trade_count == 0:
                            initial_buy = start_price
                    if z[-1] < 0 and bought == True:
                        end_price = openp[i]
                        end_buy = openp[i]
                        # print(round(z[-1],2), " Sold @ ", end_price, " ", i, sep="")
                        balance = end_price * position
                        balance = balance * (1 - (fee_level / 100))
                        bought = False
                        trade_count += 1
                        if balance < min_balance:
                            min_balance = balance
                        if balance > max_balance:
                            max_balance = balance

                if len(z) > 5:
                    z = z[1:]

        account.append(balance)

        buy_hold_return = 0
        if initial_buy > 0:
            buy_hold_return = (end_buy - initial_buy) / abs(initial_buy) * 100
        else:
            test_period = round((test_period + step), 10)
            # print("increasing test period and breaking out of loop")
            break

        account_return = (balance - starting_balance) / abs(starting_balance) * 100
        drawdown = (min_balance - max_balance) / abs(max_balance) * 100

        if account_return > highest_return:
            highest_return = account_return
            optimal_period = test_period
            optimal_buy_hold = buy_hold_return
            optimal_drawdown = drawdown
            print("file: ", f.replace("data/", ""), " | lookback: ", lookback, " | lambda: ", optimal_period,
                  " | return: ", round(highest_return, 3), "% | buy hold: ",
                  round(optimal_buy_hold, 3), "% | max drawdown: ", round(drawdown, 2), "% ", sep="")
            # print(initial_buy, end_buy)
            # print(len(z), len(close))
        test_period = round((test_period + step), 10)

    results = [f.replace("data/", ""), lookback, str(round(highest_return, 3))+"%", optimal_period, str(round(optimal_buy_hold, 3)) + "%"]
    candlestick_writer.writerow(results)

    # return highest_return, optimal_period


# final_optimized_return = -101.0
# final_optimized_period = -1.0
#
# i=1
# while i <= 100:
#     i *= 2
#     optimized_return, optimized_period = optimize(iterations=i, lookback=16)
#     if optimized_return > final_optimized_return:
#         final_optimized_return = optimized_return
#         final_optimized_period = optimized_period
#
# x = datetime.datetime.now()
# print("\n\nFinal Results:\n")
# print(final_optimized_return, final_optimized_period, x.strftime("%H:%M:%S:%f"))
#

if __name__ == "__main__":
    directory = "data"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            f = f.replace("\\", "/")
            p = multiprocessing.Process(target=optimize,
                                        kwargs={"start": 2, "end": 100, "step": 1, "lookback": 2, "f": f})
            p.start()

    # i = 2
    # while i <= 5000:
    #     optimize(start=0.0, end=1.0, step=0.01, lookback=i, directory='data')
    #     i *= 2

# optimize(start=2, end=100, step=1, lookback=2, f='data/1440_10000d.csv')
