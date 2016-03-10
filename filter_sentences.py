#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

numOfSentences = 22000000

tfile2 = codecs.open("sentences_clear","w","utf-8")
tfile = codecs.open("mk_sentences","r","utf-8-sig")

for i in range(numOfSentences):
    if i % 100000 == 0: 
	    print(str(i))
    line = tfile.readline().replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(';',' ').replace('(',' ').replace(')',' ').replace(u'„', ' ').replace(u'“',' ').replace(u'‘', ' ').replace(u'’', ' ').replace(" -", " ").replace("- ", " ").replace("'", " ").replace('"', ' ').lower()
    #sentences.append(u' '.join(line.split()))
    tfile2.write(u' '.join(line.split()) + '\r\n')
tfile.close()
tfile2.close()