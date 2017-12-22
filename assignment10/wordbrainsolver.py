# Copyright 2017 Zhonghao Guo gzh1994@bu.edu
"""Wordbrin Solver"""
from sys import argv
import numpy as np


def make_dict(length, word, dictionary):
    """Make dictionary tree based on list"""
    if length == len(word) - 1:
        dictionary.setdefault(word[length], {})['exist'] = True
    else:
        make_dict(length + 1, word, dictionary.setdefault(word[length], {}))


def start_connection(puzzle, length):
    """Make connection between words"""
    connection = [0] * (length ** 2)
    for i in range(length ** 2):
        connection[i] = [False] * (length ** 2)
    for i, j in enumerate(puzzle):
        if j == '0':
            continue
        col, row = i // length, i % length
        if row != 0:
            connection[i][i - 1] = True and puzzle[i - 1] != '0'
            if col != 0:
                connection[i][i - length -
                              1] = True and puzzle[i - length - 1] != '0'
            if col != length - 1:
                connection[i][i + length -
                              1] = True and puzzle[i + length - 1] != '0'
        if row != length - 1:
            connection[i][i + 1] = True and puzzle[i + 1] != '0'
            if col != 0:
                connection[i][i - length +
                              1] = True and puzzle[i - length + 1] != '0'
            if col != length - 1:
                connection[i][i + length +
                              1] = True and puzzle[i + length + 1] != '0'
        if col != 0:
            connection[i][i - length] = True and puzzle[i - length] != '0'
        if col != length - 1:
            connection[i][i + length] = True and puzzle[i + length] != '0'
    return connection


def search_recv(
        itr,
        length,
        lengths,
        hints,
        puzzles,
        connections,
        dictionary,
        currents,
        solution):
    """Recursive search"""
    for start, i in enumerate(puzzles):
        if i == '0':
            continue
        result = []
        unvistited = [True] * (length ** 2)
        search(
            start,
            0,
            lengths[itr],
            hints[itr],
            puzzles,
            connections,
            dictionary,
            result,
            unvistited,
            '')
        for idx in result:
            next_word = ''
            current = currents + ' '
            for i in idx:
                next_word += puzzles[ord(i)]
            current += ' ' + next_word
            if itr == len(lengths) - 1:
                solution.append(current)
            else:
                puzzle = puzzles[:]
                connection = [0] * len(puzzle)
                update_grid(puzzle, idx, length)
                connection = start_connection(puzzle, length)
                search_recv(
                    itr + 1,
                    length,
                    lengths,
                    hints,
                    puzzle,
                    connection,
                    dictionary,
                    current,
                    solution)


def hint_match(current, hints, puzzles):
    """Match hint for answer"""
    hint = {}
    for idx, i in enumerate(hints):
        if i != '*':
            hint[idx] = i
    count = 0
    next_word = ''
    for i in current:
        next_word = next_word + puzzles[ord(i)]
    for idx, i in enumerate(next_word):
        try:
            temp = hint[idx]
        except KeyError:
            continue
        if temp == i:
            count += 1
    return bool(count == len(hint))


def search(
        i,
        counter,
        length,
        hints,
        puzzle,
        connect,
        dictionary,
        result,
        unvistited,
        current):
    """Search in connection"""
    if puzzle[i] in dictionary:
        unvistited[i] = False
        current = current + chr(i)
        if counter == length - 1:
            if 'exist' in dictionary[puzzle[i]]:
                if hint_match(current, hints, puzzle):
                    result.append(current)
            return
        for itr in range(len(puzzle)):
            if connect[i][itr] and unvistited[itr]:
                search(itr, counter + 1, length, hints, puzzle, connect,
                       dictionary[puzzle[i]], result, unvistited, current)
                unvistited[itr] = True


def update_grid(puzzle, pre, length):
    """Update grid after one found"""
    for i in pre:
        puzzle[ord(i)] = '0'
    for j in range(length):
        for k in range(length):
            flag = False
            for i in range(length - 1, k - 1, - 1):
                if puzzle[j * length + i] == '0':
                    flag = True
                if puzzle[j * length + i] != '0' and flag:
                    puzzle[j *
                           length +
                           i], puzzle[j *
                                      length +
                                      i +
                                      1] = puzzle[j *
                                                  length +
                                                  i +
                                                  1], puzzle[j *
                                                             length +
                                                             i]


def main():
    """Main function"""
    small_word_list = open(argv[1], 'r').read().split()
    large_word_list = open(argv[2], 'r').read().split()
    small_dict, large_dict = {}, {}
    for word in small_word_list:
        make_dict(0, word, small_dict)
    for word in large_word_list:
        make_dict(0, word, large_dict)
    while True:
        puzzle_word_list = []
        while True:
            try:
                line = input()
            except EOFError:
                exit(0)
            if line != '':
                if '*' in line:
                    puzzles = line.split()
                    break
                else:
                    puzzle_word_list.append(list(line))
            else:
                exit(0)
        length = len(puzzle_word_list[0])
        puzzle_word_list = np.array(puzzle_word_list).T.flatten().tolist()
        lengths = [len(i) for i in puzzles]
        for i in lengths:
            i = int(i)
        solution = []
        connection = start_connection(puzzle_word_list, length)
        search_recv(
            0,
            length,
            lengths,
            puzzles,
            puzzle_word_list,
            connection,
            small_dict,
            '',
            solution)
        if len(solution) == 0:
            search_recv(
                0,
                length,
                lengths,
                puzzles,
                puzzle_word_list,
                connection,
                large_dict,
                '',
                solution)
        solution = sorted(set(solution))
        if len(solution) != 0:
            print('\n'.join(' '.join(i.split()) for i in solution))
        print('.')


if __name__ == '__main__':
    main()
