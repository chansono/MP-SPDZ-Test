#!/usr/bin/env python3

import random
from optparse import OptionParser


def main():
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)

    parser.add_option("-n", "--num_players", action="store", type="int", dest="num_players", default=3,
                      help="number of input players (default: 3)")
    parser.add_option("-s", "--size", action="store", type="int", dest="size", default=10000000,
                      help="size of input computation numbers (default: 1000000)")
    parser.add_option("-b", "--batch_size", action="store", type="int", dest="batch_size", default=0,
                      help="batch size (default: equals to the size)")
    parser.add_option("-t", "--type", action="store", type="string", dest="type", default="float",
                      help="type of data (default: float), support float/int for now")

    options, args = parser.parse_args()

    for i in range(0, options.num_players):
        file_pre = "./Player-Data/Input-P" + str(i) + "-"
        write_file(file_pre, options)


def write_file(file_pre, options):
    n_batches = 1
    batch_size = options.batch_size
    if options.batch_size <= 0:
        batch_size = options.size
    first_batch_size = batch_size
    if options.size > batch_size:
        first_batch_size = batch_size
        n_batches, mod = divmod(options.size, batch_size)
        if mod != 0:
            first_batch_size += mod

    for batch in range(n_batches):
        batch_input_file = open(file_pre + str(batch), "w", encoding="utf-8")
        curr_batch_size = batch_size if batch > 0 else first_batch_size
        for i in range(curr_batch_size):
            if i != 0:
                batch_input_file.write("\n")
            if options.type == "float":
                rand = random.uniform(0, 10000)
            elif options.type == "int":
                rand = random.randint(0, 10000)
            else:
                print("illegal data type")
                return -1
            batch_input_file.write(str(rand))
        batch_input_file.close()


if __name__ == '__main__':
    main()
