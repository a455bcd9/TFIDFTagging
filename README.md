# TFIDFTagging
TF IDF automatic tagging

http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

https://en.wikipedia.org/wiki/Tf%E2%80%93idf

```vectorize_all.py``` takes a corpus of ```.xml``` files in the ```ref``` directory (reference files) and in the ```new``` directory (files to test) as an input and returns a list of n-grams for each text of the ```new``` corpus (called tags or features).

Parameters are:
* Input files
* Desired number of tags/features for each text (variable ```best_number```)
* Maximal size of the tags: 1 (words), 2 (words or bigrams), or 3 (words, bigrams, or trigrams) (variable ```choice```)

Speed:
* If 900 files in ```ref``` and 100 files in ```new``` then it takes about 100 seconds to tag all the new files, which means about 1 s per file.