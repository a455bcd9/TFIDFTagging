import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import glob

# Corpus list
corpus = []

# Load the list of French stop words (mots vides)
stopwordsfrench = []
fileToRead = "stopwordsfrench.txt"
with open(fileToRead) as infile:
    stopwordsfrench = [word.decode('utf-8').replace("\n", "") for word in infile]

# Strings to replace
replacements = {'<br clear="none"/>':'', '<br />':'', '<br/>':'', '<br>':'', 'l\'':'', 'd\'':'', 'c\'':'', 'j\'':'', 's\'':''}

# Loop over the reference corpus (already cleaned)
for filename in glob.glob('ref/clean/*.xml'):
    # Open file, read it replace string and write in a new file line by line
    fileToWrite = filename

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

    corpus.append(p)

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

    corpus.append(p)

corpus_size = len(corpus)

#  Binary occurrence markers might offer better features: use the binary parameter of CountVectorizer

# max_df 0.5 ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words)
# min_df ?
# token_pattern=u'\w{3,}' alphanumeric strings of at least 3 characters
# token_pattern=r'\b\w+\b' bigram
word_vectorizer = TfidfVectorizer(max_df=0.9, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')
bigram_vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.9, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')
trigram_vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_df=0.9, strip_accents='ascii', stop_words=stopwordsfrench, 
    token_pattern=u'[a-zA-Z]{3,}')

# Arrays of inversed frequencies
word_array = word_vectorizer.fit_transform(corpus)
bigram_array = bigram_vectorizer.fit_transform(corpus)
trigram_array = trigram_vectorizer.fit_transform(corpus)

# List of features (words, bigrams or trigrams)
word_names = word_vectorizer.get_feature_names()
bigram_names = bigram_vectorizer.get_feature_names()
trigram_names = trigram_vectorizer.get_feature_names()

# max_indices return the indices of the N greatest elements of array a
def max_indices(a,N):
    return np.argsort(a)[::-1][:N]

# Number of features per text
best_number = 5
# List of features
tags = []

# Words, bigrams or trigrams
choice = 1
if choice == 1:
    # Loop over the corpus
    for i in range(0,corpus_size):
        # Indices of the best_number greatest frequencies of each text
        best = max_indices(word_array.toarray()[i],best_number)
        tags.append([])
        for j in range(0,best_number):
            # Feature names related to each index
            tags[i].append(word_names[int(best[j])])
elif choice == 2:
    # Loop over the corpus
    for i in range(0,corpus_size):
        # Indices of the best_number greatest frequencies of each text
        best = max_indices(bigram_array.toarray()[i],best_number)
        tags.append([])
        for j in range(0,best_number):
            # Feature names related to each index
            tags[i].append(bigram_names[int(best[j])])
elif choice == 3:
    # Loop over the corpus
    for i in range(0,corpus_size):
        # Indices of the best_number greatest frequencies of each text
        best = max_indices(trigram_array.toarray()[i],best_number)
        tags.append([])
        for j in range(0,best_number):
            # Feature names related to each index
            tags[i].append(trigram_names[int(best[j])])
else:
    print("Fuck you!")

# Print the features for the corpus
for i in range(0,corpus_size):
    print tags[i]