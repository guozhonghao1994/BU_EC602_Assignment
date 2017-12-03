// Copyright 2017 Zhonghao Guo gzh1994@bu.edu

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

std::unordered_map<int,
std::map<std::string,
std::unordered_set<std::string>>> ds;
void read_wordlist(std::string filename);
bool possible(std::string letters, std::string word, int N);
std::unordered_set<std::string> get_combos(std::string letters, int r);

int main(int argc, char const *argv[]) {
    read_wordlist(argv[1]);
    std::string letters;
    int n, r;
    std::set<std::string> word_list;
    std::unordered_set<std::string> combos;
    while (1) {
        word_list.clear();
        std::cin >> letters >> r;
        if (r == 0) {
            break;
        }
        n = letters.length();
        if (n > 20) {
            if (ds.find(r) != ds.end()) {
                for (auto letter_key : ds[r]) {
                    if (possible(letters, letter_key.first, r)) {
                        word_list.insert(letter_key.second.begin(),
                        letter_key.second.end());
                    }
                }
            }
        } else {
            if (ds.find(r) != ds.end()) {
                combos = get_combos(letters, r);
                for (auto letter_key : combos) {
                    std::sort(letter_key.begin(), letter_key.end());
                    if (ds[r].find(letter_key) != ds[r].end()) {
                        word_list.insert(ds[r][letter_key].begin(),
                        ds[r][letter_key].end());
                    }
                }
           }
        }
        for (auto const& word : word_list) {
            std::cout << word << std::endl;
        }
        std::cout << "." << std::endl;
    }
    return 0;
}

std::unordered_set<std::string> get_combos(std::string letters, int r) {
    int i, n;
    std::vector<int> v(letters.size(), 0);
    fill(v.begin(), v.begin() + r, 1);
    std::string c(r, ' ');
    std::unordered_set<std::string> thecombs;
    do {
     n = 0;
     for (i = 0; i < v.size(); i++)
       if (v[i])
         c[n++] = letters[i];
    if (thecombs.find(c) != thecombs.end())
      continue;
    thecombs.insert(c);
    } while (prev_permutation(begin(v), end(v)));
    return thecombs;
}

void read_wordlist(std::string filename) {
    std::ifstream fin;
    std::string word;
    fin.open(filename);
    int n;
    std::string letter_key;
    while (fin >> word) {
        n = word.length();
        letter_key = word;
        std::sort(letter_key.begin(), letter_key.end());
        ds[n][letter_key].insert(word);
    }
    fin.close();
}

bool possible(std::string letters, std::string word, int N) {
    int pos;
    if (word.length() != N) {
        return false;
    }
    for (auto letter : word) {
        pos = letters.find_first_of(letter);
        if (pos == -1) {
            return false;
        } else {
            letters.erase(pos, 1);
        }
    }
    return true;
}

