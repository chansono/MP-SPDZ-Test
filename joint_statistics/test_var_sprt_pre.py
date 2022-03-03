#!/usr/bin/env python3

import time
from optparse import OptionParser

time_start = time.time()

usage = "usage: %prog [options] "
parser = OptionParser(usage=usage)

parser.add_option("-p", "--player_no", action="store", type="int", dest="player_no", default=0,
                  help="player index (default: 0)")

options, args = parser.parse_args()

file_name = "./Player-Data/Input-P" + str(options.player_no) + "-0"


def read_input():
    input_file = open(file_name, "r", encoding="utf-8")
    list = []
    for line in input_file.readlines():
        list.append(float(line))
    input_file.close()
    return list


def write_result(list):
    input_file = open(file_name, "w", encoding="utf-8")
    for data in list:
        input_file.write(str(data) + "\n")
    input_file.close()


input_start = time.time()
inputs = read_input()
input_end = time.time()
print("input time: " + str(input_end - input_start) + " seconds")

final_sum = sum(inputs)
print("sum: " + str(final_sum))

sqr_sum = sum(pow(i, 2) for i in inputs)
print("sqr_sum: " + str(sqr_sum))

write_result([final_sum, sqr_sum])

time_end = time.time()
print("time elapsed: " + str(time_end - time_start) + " seconds")
