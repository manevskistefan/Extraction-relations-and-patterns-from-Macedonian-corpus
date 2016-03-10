#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import operator
import codecs
import math

#read starting pairs
pairs = []

tfile = open('pairs.txt')
lines = tfile.readlines()
for line in lines:
    pairs.append(line.lower().split())
tfile.close()


#read documents
doc_num = 1 #number of documents

for k in range(doc_num):
    tfile = open('t' + str(k) + '.txt')
 
    words = [] #all words from a document
    positions = defaultdict(list) #new empty list of positions of words
 
    i = 0
    j = 0

    for line in tfile:
        for w in line.replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace('\'',' ').replace('\"',' ').split():
            words.append(w.lower())
            positions[w.lower()].append(i)
            i += 1
        j += 1
        if j % 100000 == 0:
            print('Reading line ' + str(j) + ' of document ' + str(k+1))
        if j>1200000:
            break
 
    tfile.close()
 
 
    #find candidate relations between pairs in the given documents
 
    relations = defaultdict(int)  #frequency of middle part between pairs
    neighbourhood = []  #neighborhood found around the pairs
    neigh_size = 50  #neighborhood size (words)
 
    #process pairs
    for pair in pairs:
        print('Processing pair: ' + pair[0] + ' ' + pair[1])
        occ1 = positions[pair[0]]
        occ2 = positions[pair[1]]
        
        #neighborhood of a pair
        n = defaultdict(int)
        for i in occ1:
            for j in occ2:
                if i < j and j - i < 20:
                    #add bigrams
                    for h in range(i+1,j-1):
                        relations[' '.join(words[h:h+2])] += math.log(3)
                    #add trigrams
                    for h in range(i+1,j-2):
                        relations[' '.join(words[h:h+3])] += math.log(4)
                    #add words in between
                    r = ' '.join(words[i+1:j])
                    relations[r] += math.log(len(r)+1) 
                    #add previous words
                    if i>neigh_size:
                        prev = words[i-neigh_size:i]
                    else: 
                        prev = words[0:i]
                        for word in prev:
                            n[word] += 1
                    #add following words
                    next = words[i+1:i+1+neigh_size]
                    for word in next:
                        n[word] += 1
                    
                    #append neighborhood
                    neighbourhood.append(n)


    #output relations
    #sort by frequency
    sorted_rel = sorted(relations.items(), key=operator.itemgetter(1), reverse = True)
    #print sorted_rel[:100]

    #convert to list of strings
    sorted_rel_str = [i[0].decode('utf-8', ' ') + ' ' + str(i[1]) + '\r\n' for i in sorted_rel]
    #write to a file
    tfile = codecs.open('relations.txt','wb','utf-8')
    tfile.writelines(sorted_rel_str)
    tfile.close()

    #output neighbors
    tfile = codecs.open('neighbourhood.txt','wb','utf-8')
    #pattern matches
    matches = []

    for i in range(len(pairs)):
        #write pair
        tfile.write(pairs[i][0].decode('utf-8', ' ') + " - " + pairs[i][1].decode('utf-8', ' ') + ":\r\n")
        #sort and convert the neighborhood to list of strings
        sorted_n = sorted(neighbourhood[i].items(), key=operator.itemgetter(1), reverse = True)
        sorted_n_str = [' ' + i[0].decode('utf-8', ' ') + ' ' + str(i[1]) + '\r\n' for i in sorted_n]
        tfile.writelines(sorted_n_str)
 
        #find pattern matches
        match_words = []
        pattern = set([t[0] for t in sorted_n[:100]])
        for j in range(1000000):
            if len(pattern.intersection(words[j:j+60]))>20:
                match_words.append(words[j+30])
                matches.append(match_words) 
    tfile.close()

    #output matches
    tfile = codecs.open('matches.txt','wb','utf-8')
                    
    for i in range(len(matches)):
        tfile.write('Pair ' + str(i) + ' matches: \r\n')
        for j in range(len(matches[i])):
            tfile.write(' ' + matches[i][j].decode('utf-8', ' ') + '\r\n')
            tfile.write('\r\n')
    tfile.close()