#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import dawg
import math

tfile = codecs.open('mk_sentences','r','utf-8')

stopWords = [u'на', u'и', u'во', u'за', u'се', u'да', u'од', u'со', u'е', u'дека', u'ќе', u'што', u'не', u'го', u'ги', u'ја', u'-', u'а']

for j in range(10):
    keys = []
    values = []
    for i in range(100000):
        if i % 10000 == 0:
            print("read sentence " + str(i))
        
        line = tfile.readline().replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(';',' ').replace('(',' ').replace(')',' ').replace(u'„', ' ').replace(u'“',' ').replace(u'‘', ' ').replace(u'’', ' ').replace(" -", " ").replace("- ", " ").replace("'", " ").replace('"', ' ').lower()
        
        w = line.strip().split()
        for k in range(len(w)-1):
                ss = ' '.join(w[k:k+1])
                var = []
                
                #wildcard variations
                for jj in range(int(math.ceil(math.log(len(ss),2)))):
                 l = [ii for ii in ss]
                 for kk in range(len(ss)):
                  if (kk/2**jj)%2==0:
                   l[kk] = '*'
                 var.append(''.join(l))
                 l = [ii for ii in ss]
                 for kk in range(len(ss)):
                  if (kk/2**jj)%2==1:
                   l[kk] = '*'
                 var.append(''.join(l))
                                
                keys.append(ss)
                values.append((j*100000+i,))
                for v in var:
                 keys.append(v)
                 values.append((j*100000+i,))
                
    
    
    dtrie = dawg.RecordDAWG(">I", zip(keys,values))
    dtrie.save("dawg_bigrams_" + str(j+1))