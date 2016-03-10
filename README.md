# Extraction-relations-and-patterns-from-Macedonian-corpus
Project for the subject Natural Language Processing - Extraction relations and patterns from Macedonian corpus

1. Filtering the corpus - filter_sentences.py
	- The output corpus is write in sentences_clear
2. Making of 22 DAWG Trie structures (sentences), where each position of the word in sentences_clear has been saved
	- The output sentences are write in word-positions/dtrie_i, where i=1, to 22
3. Start to processing the pairs.txt file, which has been created previusly by the user (the pairs is splited with ' ')
	- In relations_dawg.py is the formula for patterns legth
	- In relations_dawg2.py is the formula for patterns frequency (the 10-th frequently patterns)
