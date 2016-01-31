import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Parse XML
tree = ET.parse('juriSommaireClean.xml')

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

# # Word vectorizer 1-gram
# word_vectorizer = CountVectorizer(min_df=1, strip_accents='ascii')

# # Bigram vectorizer 2-gram
# bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),
#     token_pattern=r'\b\w+\b', min_df=1, strip_accents='ascii')

# # Trigram vectorizer 3-gram
# trigram_vectorizer = CountVectorizer(ngram_range=(1, 3), 
#     min_df=1, strip_accents='ascii')

corpus = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?',
    ]
corpus_size = len(corpus)

# Decompose a string
# analyze_bigram = bigram_vectorizer.build_analyzer()
# analyze_trigram = trigram_vectorizer.build_analyzer()

# Tokens by alphabetical order
# X = word_vectorizer.fit_transform(corpus)
# print X.toarray()

# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(X)
# print tfidf.toarray()

#  Binary occurrence markers might offer better features: use the binary parameter of CountVectorizer

# max_df 0.5 ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words)
word_vectorizer = TfidfVectorizer(max_df=0.5, strip_accents='ascii')

bigram_vectorizer = TfidfVectorizer(ngram_range=(1, 2),
    token_pattern=r'\b\w+\b', max_df=0.5, strip_accents='ascii')

X_1 = word_vectorizer.fit_transform(corpus)
X_2 = bigram_vectorizer.fit_transform(corpus)
# print X_1.toarray()
# print X_2.toarray()

names = word_vectorizer.get_feature_names()
bigram_names = bigram_vectorizer.get_feature_names()
# print names
# print bigram_names

# Numpy array
# X_1_np = np.array(X_1)
# X_2_np = np.array(X_2)

def max_indices(a,N):
    return np.argsort(a)[::-1][:N]

best_number = 2
best = np.zeros((corpus_size,best_number))
tags = []

for i in range(0,corpus_size):
    best[i] = max_indices(X_1.toarray()[i],best_number)
    tags.append([])
    for j in range(0,best_number):
        tags[i].append(names[int(best[i][j])])

print tags

# ch2 = SelectKBest(chi2, k=best_number)
# X_train = ch2.fit_transform(X_train, y_train)
# X_test = ch2.transform(X_test)
# feature_names = [feature_names[i] for i in ch2.get_support(indices=True)]