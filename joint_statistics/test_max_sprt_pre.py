#!/usr/bin/env python3

import time
from concurrent.futures import ThreadPoolExecutor
from optparse import OptionParser

time_start = time.time()

usage = "usage: %prog [options] "
parser = OptionParser(usage=usage)

parser.add_option("-p", "--player_no", action="store", type="int", dest="player_no", default=0,
                  help="player index (default: 0)")
parser.add_option("-t", "--thread", action="store", type="int", dest="n_threads", default=16,
                  help="number of threads (default: 16)")
parser.add_option("-b", "--batch_size", action="store", type="int", dest="batch_size_base", default=10000,
                  help="batch size (default: 10000)")

options, args = parser.parse_args()

file_name = "./Player-Data/Input-P" + str(options.player_no) + "-0"

n_threads = options.n_threads
batch_size_base = options.batch_size_base

n_batches = 1
batch_size = 0
last_batch_size = batch_size


def prep_batches(cur_size):
    global n_batches, batch_size, last_batch_size
    n_batches = 1
    batch_size = cur_size
    n_1_size = batch_size
    if batch_size > batch_size_base:
        n_batches, mod = divmod(batch_size, batch_size_base)
        batch_size = batch_size_base
        n_1_size = batch_size
        if mod != 0:
            n_batches += 1
            n_1_size = mod


def read_input():
    input_file = open(file_name, "r", encoding="utf-8")
    # list = input_file.readlines()
    list = []
    for line in input_file.readlines():
        list.append(float(line))
    input_file.close()
    return list


def write_result(data):
    input_file = open(file_name, "w", encoding="utf-8")
    input_file.write(str(data))
    input_file.close()


input_start = time.time()
inputs = read_input()
input_end = time.time()
print("input time: " + str(input_end - input_start) + " seconds")


def max_list_in_batch():
    size = len(inputs)
    pool = ThreadPoolExecutor(max_workers=n_threads)

    def max_of_strs(list):
        return max(float(i_str) for i_str in list)

    max_list = []
    while len(max_list) == 0 or len(max_list) > batch_size_base:

        prep_batches(len(max_list) if len(max_list) > 0 else size)
        next_max_list = []

        for batch in range(n_batches):
            if len(max_list) == 0:
                future = pool.submit(max_of_strs, inputs[batch * batch_size:(batch + 1) * batch_size])
            else:
                future = pool.submit(max_of_strs, max_list[batch * batch_size:(batch + 1) * batch_size])

            def add_max(future):
                next_max_list.insert(batch, future.result())

            future.add_done_callback(add_max)

        max_list = next_max_list

    pool.shutdown()

    return max_list


final_max = max(inputs)
print("max: " + str(final_max))

write_result(final_max)

time_end = time.time()
print("time elapsed: " + str(time_end - time_start) + " seconds")
