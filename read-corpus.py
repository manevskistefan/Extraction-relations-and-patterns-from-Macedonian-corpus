#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import dawg

tfile = codecs.open('mk_sentences','r','utf-8')

stopWords = [u'на', u'и', u'во', u'за', u'се', u'да', u'од', u'со', u'е', u'дека', u'ќе', u'што', u'не', u'го', u'ги', u'ја', u'-', u'а']

for j in range(22):
	keys = []
	values = []
	for i in range(1000000):
		if i % 100000 == 0:
			print("read sentence " + str(i))
		
		line = tfile.readline().replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(';',' ').replace('(',' ').replace(')',' ').replace(u'„', ' ').replace(u'“',' ').replace(u'‘', ' ').replace(u'’', ' ').replace(" -", " ").replace("- ", " ").replace("'", " ").replace('"', ' ').lower()
        
		w = line.strip().split()
		for word in w:
			if word not in stopWords:
				keys.append(word)
				values.append((j*1000000+i,))
    
	dtrie = dawg.RecordDAWG(">I", zip(keys,values))
	dtrie.save("word-positions/dtrie_" + str(j+1))