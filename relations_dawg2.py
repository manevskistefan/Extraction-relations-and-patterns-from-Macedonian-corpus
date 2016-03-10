#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import operator
from collections import defaultdict
import dawg

#stop words
stopWords = [u'на', u'и', u'во', u'за', u'се', u'да', u'од', u'со', u'е', u'дека', u'ќе', u'што', u'не', u'го', u'ги', u'ја', u'-', u'а']

#word positions
word_positions = []

#read sentences from corpus
sentences = []

numOfSentences = 17000000
num = 17
iterations = 2

for i in range(num):
    dtrie = dawg.RecordDAWG(">I")
    word_positions.append(dtrie.load("word-positions/dtrie_" + str(i+1)))

print("read positions")

tfile = codecs.open("sentences_clear","r","utf-8-sig")
for i in range(numOfSentences):
    line = tfile.readline().strip()
    sentences.append(line)

tfile.close()
print("read sentences")

while True: 
    #pairs
    main_pairs = defaultdict(int)
	
    t = raw_input("Vnesi broj na iteracii (default=2): ")
    try:
        iterations = int(t)
    except:
        pass
    
    for iter in range(iterations): 
        print("iteration: " + str(iter+1))
        patterns = defaultdict(int)
        relations = defaultdict(int)
        neighbourhood = dict()
        newpairs = defaultdict(int)
        
        rel_pair = defaultdict(int)
        pair_rel = defaultdict(int)
        
        #read pairs
        pairs = []
        tfile = codecs.open("pairs.txt","r","utf-8-sig")
        for line in tfile:
            pair = line.rstrip().split(' ',1)
            if len(pair) == 2:
                pairs.append(pair)
        
        tfile.close()
        print("read pairs")
        
        for pair in pairs: 
            word1 = pair[0].replace("'",'').replace('"','').lower()
            word2 = pair[1].replace("'",'').replace('"','').lower()
            
            #finding the index of all the sentences that have word1
            res = []
            if word1 in stopWords: 
                set1 = "all"
            else:
                for i in range(num):
                    pos = word_positions[i].get(word1)
                    if pos:
                        res.extend(pos) 
                    
                set1 = set([j[0] for j in res])
            
            print("fetched set 1")
            
            #finding the index of all the sentences that have word2
            res = []
            if word2 in stopWords: 
                set2 = "all"
            else: 
                for i in range(num):
                    pos = word_positions[i].get(word2)
                    if pos:
                        res.extend(pos) 
                    
                set2 = set([j[0] for j in res])
            
            print("fetched set 2")
         
            #finding the index of all the sentences that have word1 and word2 at same time
            if set1 == "all" and set2 == "all": 
                setf = set()
            elif set1 == "all": 
                setf = set2
            elif set2 == "all": 
                setf = set1
            else: 
                setf = set1.intersection(set2)
            
            print("created subset")
            
            #iterate all sentences which indexes are in setf
            for i in setf:
                sentence = sentences[i] + " "
                words = sentence.rstrip().split(' ',1)
                order = 0
                
                #indexes of word1 and word2 in sentence
                occ1 = sentence.find(word1+' ') 
                occ2 = sentence.find(word2+' ') 
                
                if occ1 != -1 and occ2 != -1: 
                    if occ1>occ2: 
                        p = occ1
                        occ1 = occ2
                        occ2 = p
                        order = -1
                    
                    #if word1 is before word2, then r is relation that starts from word1 to word2 (without them)
                    if order == 0:
                        r = sentence[occ1+len(word1):occ2-1]
                        suff = sentence[occ2+len(word2)+1:].split(' ',3)[:3]
                    else:
                        r = sentence[occ1+len(word2):occ2-1]
                        suff = sentence[occ2+len(word1)+1:].split(' ',3)[:3]
                    
                    pref = sentence[:occ1-1].rsplit(' ',3)[-3:]
                    
                    pref = ' '.join(pref).strip()
                    suff = ' '.join(suff).strip()
                    
                    r=r.strip()
                    
                    #relation must be less then 55
                    if len(r) < 55:
                        relations[r] += 1
                    
                    #all prefixes and suffixes of the relation r
                    if r in neighbourhood:
                        neighbourhood[r].append([pref,suff])
                    else:
                        neighbourhood[r] = [[pref,suff]]
                        
                    pair_rel[word1 + ' ' + word2 + ' -> ' + pref + '*' + r + '*' + suff] += 1
            
            print("found relations")

        #sort by frequency
        sorted_rel = sorted(relations.items(), key=operator.itemgetter(1), reverse = True)
        sorted_rel = sorted_rel[:  int(len(sorted_rel) / 3)]

        #convert to strings
        sorted_rel_str = [i[0] + ' ' + str(i[1]) + '\r\n' for i in sorted_rel]

        #write to a file
        tfile = codecs.open('relations.txt','wb','utf-8-sig')
        tfile.writelines(sorted_rel_str)
        tfile.close()

        for r in sorted_rel:
            for n in neighbourhood[r[0]]:
                pattern = n[0] + '*' + r[0] + '*' + n[1]
                patterns[pattern] += 1

        #sort by frequency
        sorted_patterns = sorted(patterns.items(), key=operator.itemgetter(1), reverse = True)
        sorted_patterns = sorted_patterns[:10]

        #convert to strings
        tmpPatterns = list()
        for i in sorted_patterns: 
            tmpPatterns.append(i[0] + ' ' + str(i[1]) +'\r\n')

        #write to a file
        tfile = codecs.open('patterns.txt','wb','utf-8-sig')
        tfile.writelines(tmpPatterns)
        tfile.close()

        #find new pairs from relations
        for rel in sorted_patterns: 
            setf = set()
            words = []
            for i in rel[0].split("*"): 
                for j in i.split():
                    if j not in stopWords: 
                        words.append(j)
                
            for i,r in enumerate(words):
                if i < 6:
                    r = r.replace("'",'').replace('"','')
                    res = []
                    
                    for j in range(num):
                        pos = word_positions[j].get(r)
                        if pos:
                            res.extend(pos) 
                    
                    if i==0:
                        setf = set([i[0] for i in res])
                    else:
                        setf = setf.intersection(set([i[0] for i in res]))                    
            
            print("found relation occurences")
                
            for i in setf:
                sentence = ' ' + sentences[i] + ' '
                order = 0
                [p,m,s] = rel[0].split('*')
                    
                occp = sentence.find(' ' + p + ' ')
                occm = sentence.find(' ' + m + ' ')
                occs = sentence.find(' ' + s + ' ')
                    
                left = ""
                right = ""
                try: 
                    if occp != -1 and occm!=-1 and occs!=-1: 
                        left = sentence[occp+len(p)+2:occm]
                        right = sentence[occm+len(m)+2:occs]
                    elif p == "" and occp == -1 and occm!=-1 and occs!=-1 and occm+len(m) < len(sentence): 
                        left = sentence[:occm].rsplit()[-1]
                        right = sentence[occm+len(m)+2:occs]
                    elif m == "" and occp != -1 and occm == -1 and occs!=-1: 
                        left = sentence[occp+len(p)+2:occs].split()[0]
                        right = sentence[occp+len(p)+2:occs].split()[-1]
                    elif s == "" and occp != -1 and occm!=-1 and occs == -1 and occm+len(m) < len(sentence): 
                        left = sentence[occp+len(p)+2:occm]
                        right = sentence[occm+len(m)+2:].split()[0]
                except: 
                    pass
                
                if len(left) > 1 and len(right) > 1 and len(left) < 35 and len(right) < 35:
                    newpairs[left + " " + right] += 1
                    main_pairs[left + " " + right] += 1
                    rel_pair[p + '*' + m + '*' + s + ' -> ' + left + ' ' + right]+=1
                
            print("found new pairs")
        
        tfile.close()

        #sort by frequency
        sorted_newp = sorted(newpairs.items(), key=operator.itemgetter(1), reverse = True)
        sorted_main_pairs = sorted(main_pairs.items(), key=operator.itemgetter(1), reverse = True)
        
        #convert to strings
        sorted_newp_str = [i[0] + '\r\n' for i in sorted_newp]
        sorted_newp_count = [i[0] + ' ' + str(i[1]) +'\r\n' for i in sorted_newp]
        sorted_main_pairs_str = [i[0] + '\r\n' for i in sorted_main_pairs]
        
        #write the new pairs from current iteration
        tfile = codecs.open('newpairs_iter' + str(iter+1) + '.txt','wb','utf-8-sig')
        tfile.writelines(sorted_newp_count)
        tfile.close()
        
        #write pairs
        tfile = codecs.open('pairs.txt','wb','utf-8-sig')
        tfile.writelines(sorted_main_pairs_str)
        tfile.close()
        
        #write pair-relation map to a file
        sorted_pair_rel = [i[0] + ' ' + str(i[1]) + '\r\n' for i in pair_rel.items()]
        tfile = codecs.open('pair_relation_iter' + str(iter+1) + '.txt','wb','utf-8-sig')
        tfile.writelines(sorted_pair_rel)
        tfile.close()
        
        #write relation-pair map to a file
        sorted_rel_pair = [i[0] + ' ' + str(i[1]) + '\r\n' for i in rel_pair.items()]
        tfile = codecs.open('relation_pair_iter' + str(iter+1) + '.txt','wb','utf-8-sig')
        tfile.writelines(sorted_rel_pair)
        tfile.close()

    raw_input('Stisni enter za testiranje so novi parovi...')