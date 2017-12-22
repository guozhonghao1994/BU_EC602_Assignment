// Copyright 2017 Zhonghao Guo gzh1994@bu.edu
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using std::cout;
using std::string;
using std::vector;
using std::cin;
using std::endl;
using std::sort;
class TrieNode {
 public:
  TrieNode* children[26] = {NULL};
};
class MyTrie {
 public:
  TrieNode *root = new TrieNode();
  void insert(string *s) {
    TrieNode *cur = root;
    TrieNode *next;
    for (char c : (*s)) {
      if (cur->children[c - 'a'] != NULL) {
        next = (cur->children)[c - 'a'];
      } else {
        next = new TrieNode();
        (cur->children)[c - 'a'] = next;
      }
      cur = next;
    }
  }
  bool find(string s) {
     return helper(root, s, 0);
  }
  bool helper(TrieNode* root, string s, int layer){
    if (layer == s.length()) {
      return true;
    }
    if (root->children[s[layer]-'a']!= NULL) {
      return helper(root->children[s[layer]-'a'], s, layer+1);
    }
    return false;
  }
};
class Coordinate{
 public:
  int x;
  int y;
  Coordinate(int x, int y){
    this->x = x;
    this->y = y;
  }
};
MyTrie* smallwordlist[30] = {NULL};
MyTrie* largewordlist[30] = {NULL};
int Direction[8][2] = {{0,1}, {1,0}, {0,-1}, {-1,0}, {1,1}, {1,-1}, {-1,1}, {-1,-1}};
bool isValid(vector<vector<char>>*matrix, int x, int y, vector<vector<bool>>&visited){
  return x<matrix->size() && x>=0 && y < (*matrix)[0].size() && y >= 0 && (*matrix)[x][y] != '*' && (visited[x][y] == false);
}
vector<vector<char>> reconstruct(vector<vector<char>>*matrix, vector<Coordinate>list){
  vector<vector<char>> results(*matrix);   
  for(Coordinate c:list){                 
    results[c.x][c.y]='*';
  }
  for(int i=0; i<results.size(); i++){   
    for(int j=0; j<results[0].size(); j++){
      if(i+1 <results.size() && results[i+1][j] == '*') {
        for(int k=i; k>=0 ; k--) {
            char temp = results[k][j];
            results[k][j] = results[k+1][j];
            results[k+1][j] = temp;
        }
      }
    }
  }
  return results;
}
void DFSHelper (vector<vector<bool>> &visited, vector<vector<char>>* matrix, string pivot, int x,
  int y, vector<vector<Coordinate>> &result, int layer, vector<Coordinate>list, string s, MyTrie* wordlist[]){
       if(pivot[layer] != '*' && (*matrix)[x][y] != pivot[layer]){
        return;
       }
       if(layer == pivot.length()-1) {
        if(wordlist[pivot.length()]->find(s)){
          vector<Coordinate> temp(list);
          result.push_back(temp);
          return;
        }
       }
       for(int i=0; i<8; i++) {
        int nextx = x + Direction[i][0];
        int nexty = y + Direction[i][1];
        if(!isValid(matrix, nextx, nexty, visited)){ 
          continue;
        }
        s.push_back((*matrix)[nextx][nexty]);
        if(wordlist[pivot.length()]->find(s)){
          visited[x][y]=true;
          list.push_back(Coordinate(nextx,nexty));
          DFSHelper(visited, matrix, pivot, nextx, nexty, result, layer+1, list, s, wordlist);
          list.pop_back();
          visited[x][y]=false;
        }
        s.pop_back();
       }
}
vector<vector<Coordinate>> couldFind(vector<vector<char>>*matrix, string pivot, int x, int y, MyTrie* wordlist[]){
  vector<vector<bool>> visited(matrix->size(),vector<bool>((*matrix)[0].size(),false));
  vector<vector<Coordinate>>result;
  string s;
  s.push_back((*matrix)[x][y]);          
  vector<Coordinate>list;
  list.push_back(Coordinate(x,y));
  DFSHelper(visited, matrix, pivot, x, y, result, 0, list, s, wordlist);
  return result;
}
void findResult(vector<vector<string>>&result, vector<vector<char>>*matrix, 
  vector<string>number, int layer, vector<string>&list, MyTrie* wordlist[]){
  for (string s : number) {
  	if(wordlist[s.length()] == NULL) {
  		return;
  	}
  }
  if(layer == number.size()){ 
    vector<string>temp;    
    for(string s : list){
      temp.push_back(s);      
    }
    result.push_back(temp);
  }
  for(int i=0; i<matrix->size(); i++){
     for(int j=0; j<(*matrix)[0].size(); j++){
      if((*matrix)[i][j] == '*'){
        continue;
      }
      vector<vector<Coordinate>>results =couldFind(matrix, number[layer], i, j, wordlist);
      if(!results.empty()){
         for(vector<Coordinate> Clist : results){
          string s;
          for(Coordinate c: Clist){
            s.push_back((*matrix)[c.x][c.y]);
          }
          list.push_back(string(s));
          vector<vector<char>>newmatrix = reconstruct(matrix, Clist);
          findResult(result, &newmatrix, number, layer+1, list, wordlist);
          list.pop_back();
         }
      }
     }
  }
}

void readfromfile(string s, MyTrie* wordlist[]){
  std::ifstream in(s);
  string line;
  int var;
  while (getline(in, line)) {
    var = line.length();
    if (wordlist[var] == NULL) {
      MyTrie *newtrie = new MyTrie();
      newtrie->insert(&line);
      wordlist[var] = newtrie;
    } else {
      wordlist[var]->insert(&line);
    }
  }
}
vector<string> split(const string& s, const char& c)
{
    string buff{""};
    vector<string> v;

    for(auto n:s)
    {
        if(n != c) buff+=n; 
        else if(n == c && buff != "") { v.push_back(buff); buff = ""; }
    }
    if(buff != "") v.push_back(buff);

    return v;
}
int main(int argc, char const *argv[]){
   readfromfile(argv[1],smallwordlist);
   readfromfile(argv[2],largewordlist);
   vector<vector<char>>input;
  string str;
  while(!cin.eof()){
    vector<vector<char>>input;
    getline(cin,str);
    input.push_back(vector<char>());
    for(int i=0; i<str.length(); i++){
     input[0].push_back(str[i]);
    }
    for(int i=0; i<str.length()-1; i++){
     getline(cin,str);
     input.push_back(vector<char>());
     for(int j=0; j<str.length(); j++){
      input[i+1].push_back(str[j]);
     }
    }
    getline(cin,str);
    vector<string>number = split(str,' ');
    vector<vector<string>> result = vector<vector<string>>();
    vector<string>list;
    findResult(result, &input, number, 0, list, smallwordlist);
    if(result.empty()){
      findResult(result,&input,number,0, list, largewordlist);
    }
    if(result.empty()){
      cout<<"."<<endl;
    } else {
      sort(result.begin(), result.end());
      vector<vector<string>> cons;
      cons.push_back(result[0]);
      for (int i = 1; i < result.size(); i++) {
        if (result[i] != result[i - 1]) {
          cons.push_back(result[i]);
        }
      }
      for (vector<string> v : cons) {
        for (string s : v) {
          std::cout << s << " ";
        }
        std::cout << std::endl;
      }
      std::cout << "." << std::endl;
    }
  }
  return 0;
}
