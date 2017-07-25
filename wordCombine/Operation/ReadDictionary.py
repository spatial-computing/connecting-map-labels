#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import glob
import operator
path = '../resources/AllStates_20170601'
#path = '../resources/test'

def read_from_folder():


    for filename in os.listdir(path):
        wordSet={}
        filename = path+'/'+filename
        print filename
        with open(filename) as f:
            next(f)
            for line in f:
                bufferArr = line.split('|')
                name = bufferArr[1].replace(' (historical)','')
                name = name.replace('(', '')
                name = name.replace(')', '')
                name = name.lower()
                wordArr = name.split(" ")
                endingWord = wordArr[len(wordArr)-1]
                if endingWord.isdigit():
                    continue
                if endingWord in wordSet:
                    wordSet[endingWord] += 1
                else:
                    wordSet[endingWord] =1

        wordSet= sorted(wordSet.items(), key=operator.itemgetter(1),reverse=True)
        writefile = open('../resources/nameFile.txt', "a")
        for word in wordSet:
            #print word
            if word[1]>5:
                writefile.write(word[0]+"::::"+str(word[1])+"\n")

        writefile.close()
        #print "%s: %s" %(word,wordSet[word])

    # infile = open(filename, 'r')
    # firstLine = infile.readline()
    # firstLine = infile.readline()


def read_from_data():
    d = {}
    with open("../resources/nameFile.txt") as f:
        for line in f:
            #print line
            (key, val) = line.split("::::")
            if key in d:

                d[key] += int(val)
            else:
                d[key] = int(val)
    f.close()
    d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    writefile = open('../resources/final.txt', "w")
    for k in d:
        print k
        if not k[0].isdigit():
            writefile.write(k[0]+"::::"+str(k[1])+"\n")
    writefile.close()


def get_dictionary():
    wordlist=[]
    with open("../resources/nameFile.txt") as f:
        for line in f:
            #print line
            (key, val) = line.split("::::")
            if val >30:
                wordlist+=key
    return wordlist



if __name__ == '__main__':

    #read_from_folder()
    read_from_data()