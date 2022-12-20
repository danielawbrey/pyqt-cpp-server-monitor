#ifndef HELPER
#define HELPER

#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <sstream>
#include <vector>
#include <unistd.h>

using namespace std;

string convertArrayToString(char arr[], int n) {
    string str = "" ;
    for (int i = 0 ; i < n ; i++ ) {
        str.push_back(arr[i]);
    }

    return str;
}

vector<string> splitString(string str) {
    vector<string> v;
    stringstream ss(str);

    while (ss.good()) {
        string substr;
        getline(ss, substr, ';');
        v.push_back(substr);
    }

    return v;
}

bool stringIsDigit(string line) {
    char* p;
    strtol(line.c_str(), &p, 10);
    return *p == 0;
}

vector<string> getDescriptionParts(vector<string> testParts) {
    vector<string> v;
    for(int i = 0; i < testParts.size(); i++) {
        string s =  testParts[i];
        stringstream ss(s);
        while (ss.good()) {
            getline(ss, s, '=');
            if(stringIsDigit(s) && s != " ")
                v.push_back(s);
        }
    }

    return v;       
}

#endif