import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import glob
from time import time

# For timer
t0 = time()

# Create the corpus list
corpus = []

# Load the list of French stop words (mots vides)
stopwordsfrench = []
fileToRead = "stopwordsfrench.txt"
with open(fileToRead) as infile:
    stopwordsfrench = [word.decode('utf-8').replace("\n", "") for word in infile]

# Strings to replace
replacements = {'<br clear="none"/>':'', '<br />':'', '<br/>':'', '<br>':'', 'l\'':'', 'd\'':'', 'c\'':'', 
    'j\'':'', 's\'':'', 'quelqu\'un':'', 'aujourd\'hui':''}

# Loop over the reference corpus (already cleaned)
for filename in glob.glob('ref/clean/*.xml'):
    # Open file, read it replace string and write in a new file line by line
    fileToRead = filename
    # fileToWrite = filename.split("/")[0] + '/clean/' + filename.split("/")[1]

    # with open(fileToRead) as infile, open(fileToWrite, 'w') as outfile:
    #     for line in infile:
    #         for src, target in replacements.iteritems():
    #             line = line.replace(src, target)
    #         outfile.write(line)

    # Parse XML
    tree = ET.parse(fileToRead)

    # Get the root of the XML
    root = tree.getroot()

    # Down the tree TEXTE then BLOC_TEXTUEl then CONTENU
    texte = root.find('TEXTE')
    bloc_textuel = texte.find('BLOC_TEXTUEL')
    contenu = bloc_textuel.find('CONTENU')

    # Get text from children from CONTENU = paragraphs <p></p>
    p = ''
    for child in contenu:
        p = p + child.text

    # Add new text to the corpus
    corpus.append(p)

# Size of the reference corpus
reference_corpus_size = len(corpus)

# Loop over the new corpus (need to be cleaned)
for filename in glob.glob('new/*.xml'):
    # Open file, read it replace string and write in a new file line by line
    fileToRead = filename
    fileToWrite = filename.split("/")[0] + '/clean/' + filename.split("/")[1]

    with open(fileToRead) as infile, open(fileToWrite, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)

    # Parse XML
    tree = ET.parse(fileToWrite)

    # Get the root of the XML
    root = tree.getroot()

    # Down the tree TEXTE then BLOC_TEXTUEl then CONTENU
    texte = root.find('TEXTE')
    bloc_textuel = texte.find('BLOC_TEXTUEL')
    contenu = bloc_textuel.find('CONTENU')

    # Get text from children from CONTENU = paragraphs <p></p>
    p = ''
    for child in contenu:
        p = p + child.text

    # Add new text to the corpus
    corpus.append(p)

# Total size of the corpus: reference + new texts
corpus_size = len(corpus)

#  Binary occurrence markers might offer better features: use the binary parameter of CountVectorizer

# max_df: ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words)
# min_df: ignore terms that have a document frequency strictly lower than the given threshold
# token_pattern=u'\w{3,}' alphanumeric strings of at least 3 characters
# token_pattern=r'\b\w+\b' bigram
word_vectorizer = TfidfVectorizer(max_df=0.4, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')
bigram_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.5, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')
trigram_vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_df=0.5, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')

# max_indices return the indices of the N greatest elements of array a
def max_indices(a,N):
    return np.argsort(a)[::-1][:N]

# Number of features per text
best_number = 10
# List of features
tags = []

# Words, bigrams or trigrams
max_gram = 1
if max_gram == 1:
    # Arrays of inversed frequencies
    freq = word_vectorizer.fit_transform(corpus)
    # List of features (words, bigrams or trigrams)
    feature_names = word_vectorizer.get_feature_names()
elif max_gram == 2:
    # Arrays of inversed frequencies
    freq = bigram_vectorizer.fit_transform(corpus)
    # List of features (words, bigrams or trigrams)
    feature_names = bigram_vectorizer.get_feature_names()
elif max_gram == 3:
    # Arrays of inversed frequencies
    freq = trigram_vectorizer.fit_transform(corpus)
    # List of features (words, bigrams or trigrams)
    feature_names = trigram_vectorizer.get_feature_names()
else:
    print("Choose a max_gram!")

if (1 <= max_gram <= 3):
    # Loop over the corpus
    for i in range(reference_corpus_size,corpus_size):
        # Indices of the best_number greatest frequencies of each text
        best = max_indices(freq.toarray()[i],best_number)
        tags.append([])
        for j in range(0,best_number):
            # Feature names related to each index
            tags[i-reference_corpus_size].append(feature_names[int(best[j])])
else:
    print("Choose a max_gram!")

# Print the features for the corpus
for i in range(0,corpus_size-reference_corpus_size):
    print tags[i]

duration = time() - t0
print("done in %fs" % duration)