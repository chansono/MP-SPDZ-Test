#!/usr/bin/python3

from optparse import OptionParser
import numpy as np
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot


def prepare_dataset(x, y):
    # reshape to be [samples][pixels][width][height]
    x = x.reshape(x.shape[0], 28, 28, 1)
    y = y.reshape(y.shape[0], 1)

    # convert from int to float
    x = x.astype('float32')

    num_wanted = 0
    x_wanted = []
    y_wanted = []
    for i in range(x.shape[0]):
        image = x[i, :]
        label = y[i]
        if label in digits:
            x_wanted.append(image)
            y_wanted.append(label)
            num_wanted += 1
    x_final = np.array(x_wanted)
    y_final = np.array(y_wanted)
    x_final = x_final.reshape((num_wanted, 28, 28, 1))
    y_final = y_final.reshape((num_wanted, 1))

    return x_final, y_final


# Augmentation
def augment(x, y, n, batch_size=1000):
    data = []
    batches = 0
    count = 0
    for x_batch, y_batch in datagen.flow(x, y, batch_size=batch_size):
        x_batch = x_batch.reshape(x_batch.shape[0], 28 * 28)
        y_batch = y_batch.reshape(y_batch.shape[0], 1)
        cur_batch_size = x_batch.shape[0]

        if batches >= n / batch_size and count + cur_batch_size >= n:
            cur_batch_size = n - count
            count = n
        else:
            count += cur_batch_size

        for j in range(0, cur_batch_size):
            data.append(x_batch[j, :])
            print(int(y_batch[j, 0] == digits[1]), end=' ')

        batches += 1
        if batches >= n / batch_size and count >= n:
            # we need to break the loop by hand because the generator loops indefinitely
            break

    for x in data:
        for y in x:
            print(y, end=' ')
        print()


# test for retrieve one batch of images
def view_figure(datagen, x, y, batch_size=9):
    for x_batch, y_batch in datagen.flow(x, y, batch_size=batch_size):
        # create a grid of 3x3 images
        for i in range(0, 9):
            pyplot.subplot(330 + 1 + i)
            pyplot.imshow(x_batch[i].reshape(28, 28), cmap=pyplot.get_cmap('gray'))
        # show the plot
        pyplot.show()
        break


usage = "usage: %prog [options] "
parser = OptionParser(usage=usage)
parser.add_option("-n", "--num_train", action="store", type="int", dest="num_train", default=20000)
parser.add_option("-s", "--num_test", action="store", type="int", dest="num_test", default=4000)
options, args = parser.parse_args()

# load data
(x_train_origin, y_train_origin), (x_test_origin, y_test_origin) = mnist.load_data()

# filter 0/1
digits = 0, 1

x_train, y_train = prepare_dataset(x_train_origin, y_train_origin)
x_test, y_test = prepare_dataset(x_test_origin, y_test_origin)

# define data preparation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    rescale=1. / 255)

# fit parameters from data
datagen.fit(x_train)
datagen.fit(x_test)

augment(x_train, y_train, options.num_train)
augment(x_test, y_test, options.num_test)

# view_figure(datagen, x_train, y_train)
