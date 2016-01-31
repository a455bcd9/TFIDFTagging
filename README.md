# TFIDFTagging
TF IDF automatic tagging

http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

https://en.wikipedia.org/wiki/Tf%E2%80%93idf

'''vectorize.py''' takes a corpus of '''.xml''' files as an input and returns a list of n-grams for each text of the corpus (called tags or features).

Parameters are:
* Input files
* Desired number of tags/features for each text (variable '''best_number''')
* Maximal size of the tags: 1 (words), 2 (words or bigrams), or 3 (words, bigrams, or trigrams) (variable '''choice''')