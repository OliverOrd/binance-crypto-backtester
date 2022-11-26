import csv
from numpy import genfromtxt
import datetime
import sys
import os
import csv

# csvfile = open('data/40.csv', 'w', newline='')
# writer = csv.writer(csvfile, delimiter=',')
#
# old = genfromtxt('data/1.csv', delimiter=',')
#
# second = int(datetime.datetime.utcfromtimestamp(int(old[1][0]) / 1000).strftime('%M'))
#
# new_timeframe = []
#
# for i in range(len(old)):
#     second_value = int(datetime.datetime.utcfromtimestamp(int(old[i][0]) / 1000).strftime('%M'))
#     if second_value % 40 == 0:
#         new_timeframe.append(old[i])
#
# for data in new_timeframe:
#     writer.writerow(data)

if __name__ == "__main__":

    directory = "results"
    results = []
    try:
        os.remove('results/final_results.csv')
    except:
        pass

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            f = f.replace("\\", "/")
            print(f)
            # old = genfromtxt(f, delimiter=',')
            with open(f) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    results.append(row)
            os.remove(f)

    csvfile = open('results/final_results.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')
    for data in results:
        writer.writerow(data)