# Copyright 2017 Zhonghao Guo gzh1994@bu.edu
import hashlib
from os import listdir
import re
import sys
from skimage.io import imread
import numpy as np


def make_transforms(img):
    transform_list = []
    transform_list.append(hashlib.sha256(bytes(img)).hexdigest())
    turn_0_mirror = img[::1, ::-1]
    turn_0_mirror_hash = hashlib.sha256(bytes(turn_0_mirror)).hexdigest()
    transform_list.append(turn_0_mirror_hash)
    turn_90 = np.transpose(img[::-1, ])
    turn_90_hash = hashlib.sha256(bytes(turn_90)).hexdigest()
    transform_list.append(turn_90_hash)
    turn_90_mirror = np.transpose(img)
    turn_90_mirror_hash = hashlib.sha256(bytes(turn_90_mirror)).hexdigest()
    transform_list.append(turn_90_mirror_hash)
    turn_180 = img[::-1, ::-1]
    turn_180_hash = hashlib.sha256(bytes(turn_180)).hexdigest()
    transform_list.append(turn_180_hash)
    turn_180_mirror = img[::-1]
    turn_180_mirror_hash = hashlib.sha256(bytes(turn_180_mirror)).hexdigest()
    transform_list.append(turn_180_mirror_hash)
    turn_270 = np.transpose(img[::1, ::-1])
    turn_270_hash = hashlib.sha256(bytes(turn_270)).hexdigest()
    transform_list.append(turn_270_hash)
    turn_270_mirror = np.transpose(img[::-1, ::-1])
    turn_270_mirror_hash = hashlib.sha256(bytes(turn_270_mirror)).hexdigest()
    transform_list.append(turn_270_mirror_hash)
    return frozenset(transform_list)


def main():
    files = []
    for file in listdir():
        if file.endswith(".png"):
            files.append(file)
    answer_list = {}
    for png in files:
        img = 1-imread(png, as_grey=True)
        data = np.nonzero(img)
        img = img[min(data[0]):max(data[0])+1, min(data[1]):max(data[1])+1]
        shape = make_transforms(img)
        if shape in answer_list.keys():
            answer_list[shape].append(png)
        else:
            answer_list[shape] = [png]
    order = []
    regex = re.compile(r'\d+')

    for i in answer_list.keys():
        order.append(answer_list[i])
    length_order = len(order)
    for j in range(length_order):
        for k in range(len(order[j])):
            num = regex.findall(order[j][k])
            num = int(num[0])
            order[j][k] = (num, order[j][k])

    to_write = sorted(order)
    length_to_write = len(to_write)

    for number in range(length_to_write):
        to_write[number] = sorted(to_write[number])
    to_write = sorted(to_write)
    with open(sys.argv[1], "w") as text_file:
        for number2 in range(length_to_write):
            for number3 in range(len(to_write[number2])):
                if number3 == len(to_write[number2])-1:
                    text_file.write(to_write[number2][number3][1])
                else:
                    text_file.write(to_write[number2][number3][1] + " ")
            text_file.write("\n")

    has = open(sys.argv[1], 'r')
    data2 = has.read()
    done = hashlib.sha256(bytes(data2, 'utf-8')).hexdigest()
    has.close()

    print(done)
    return done
if __name__ == '__main__':
    main()
