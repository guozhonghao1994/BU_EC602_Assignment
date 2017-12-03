# Copyright 2017 Zhonghao Guo gzh1994@bu.edu

import sys
import itertools


def possible(word, letters, N):
    if len(word) != N:
        return False
    for char in word:
        if char not in letters:
            return False
        bank = letters.replace(char, "", 1)
        if len(bank) != len(letters)-1:
            return False
        else:
            letters = bank
    return True

with open(sys.argv[1], 'r') as r:
    words = list(map(tuple, r.read().split()))
alg1_words = {}
alg2_words = {}
for word in words:
    n = tuple(sorted(word))
    x = len(word)
    if x in alg1_words:
        alg1_words[x].add(word)
    else:
        alg1_words[x] = set()
        alg1_words[x].add(word)
    if n in alg2_words:
        alg2_words[n].add(word)
    else:
        alg2_words[n] = set()
        alg2_words[n].add(word)

while(True):
    letters, r = input().split()
    r = int(r)
    if r == 0:
        break
    l2 = tuple(sorted(letters))
    if (len(letters)-r > 5):
        if (r in alg1_words):
            word_lst = sorted([''.join(word)
                               for word in alg1_words[r]
                               if possible(word,
                               letters, r)])
            if len(word_lst) != 0:
                print(*word_lst, sep='\n')
    else:
        word_lst = [list(map(''.join, alg2_words[combo]))
                    for combo in itertools.combinations(l2, r)
                    if combo in alg2_words]
        if len(word_lst) != 0:
            print(*sorted(set(itertools.chain.from_iterable(word_lst))),
                  sep='\n')
    print('.')
