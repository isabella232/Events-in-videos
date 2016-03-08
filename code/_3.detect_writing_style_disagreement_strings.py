import re, collections
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity 


label_count_file = '_2 label_counts.csv'

stop = stopwords.words('english')
stemmer = PorterStemmer()

def words(text): return re.findall('[a-z]+', text.lower()) 

def levenshtein(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows. '''
    if s == t: return 0
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big_spellcheck.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def correctWords(words):
    return [correct(word) for word in words]

def clean(text):
    regex = re.compile("[^\w']")
    text = regex.sub(' ', text)
    while '  ' in text:
        text = text.replace('  ',' ')
    return text.lower().strip()

def removeStopwords(words):
    return [word for word in words if word not in stop]
    
def stem(words):
    return [stemmer.stem(word) for word in words]

def filterType(words):
    newWords = []
    for word in words:
        if word.strip().lower() == 'type':
            break
        newWords.append(word)
    return newWords


def merge_space_separated(words,all_words):
    merge_space_separated_words = []
    previous_matched = False
    if len(words) == 1:
        merge_space_separated_words = words
    for i in range(1, len(words)):
        previous_word = words[i-1]
        word = words[i]
        merged = previous_word+word
        if previous_matched:
            if i == len(words)-1:
                merge_space_separated_words.append(word)
                previous_matched = True
            else:
                previous_matched = False
        else:
            if merged in all_words:
                merge_space_separated_words.append(merged)
                previous_matched = True
            elif i == len(words)-1:
                merge_space_separated_words.append(previous_word)
                merge_space_separated_words.append(word)
            else:
                merge_space_separated_words.append(previous_word)
                previous_matched = False
    return merge_space_separated_words
        
def swap_spaced_words(words, spaced_words):
    for i in range(0,len(words)-1):
        word = words[i]
        word2 = words[i+1]
        if word2+' '+word in spaced_words:
            swapped_count = spaced_words[word2+' '+word]
            normal_count = spaced_words[word+' '+word2]
            if swapped_count > normal_count:
                words[i] = word2
                words[i+1] = word
    return words


def calc_similarity(label1, label2):
    words1 = label1.split(' ')
    words2 = label2.split(' ')
    vector1 = words_to_vector(words1)
    vector2 = words_to_vector(words2)
    cosine = get_cosine(vector1, vector2)
    return cosine
            
    
def get_highest_words(words, tfidf_matrix, tfidf_train_set, all_labels, debug):
    #TODO, Check Big > Small aswell
    label = ' '.join(words)
    highest = 0
    best_label = label
    train_index = tfidf_train_set.index(label)
    cosine = cosine_similarity(tfidf_matrix[train_index], tfidf_matrix)[0]
    for i in range(0, len(cosine)):
        cos = cosine[i]
        other_label = tfidf_train_set[i]
        other_count = all_labels[other_label]
        if cos * other_count > highest:
            highest = cos * other_count
            best_label = other_label   
    return best_label.split(' ')


def clean_label(label):
    label = clean(label)
    label = label.split(' ')
    label = removeStopwords(label)
    label = stem(label)
    label = ' '.join(label)
    return label

f = open(label_count_file, 'r')
label_counts = {}
for line in f.readlines()[1:]:
    info = line.strip().split('|')
    label = info[0]
    count = int(info[1])
    label_counts[label] = count
f.close()

translations = {}
cleaned_labels = {}
labels = label_counts.keys()
for label in labels:
    cleaned_label = clean_label(label)
    cleaned_labels[label] = cleaned_label
    
for i in range(0, len(labels)-1):
    for j in range(i+1, len(labels)):
        label_1 = labels[i]
        label_2 = labels[j]
        cleaned_label_1 = cleaned_labels[label_1]
        cleaned_label_2 = cleaned_labels[label_2]
        label_count_1 = label_counts[label_1]
        label_count_2 = label_counts[label_2]
        if cleaned_label_1 == cleaned_label_2 or set(cleaned_label_1.split(' ')) == set(cleaned_label_2.split(' ')):
            if label_count_1 > label_count_2:#Label 2 becomes label 1
                label_from = label_2
                label_to = label_1
            else:#label 1 becomes label 2
                label_from = label_1
                label_to = label_2
            translations[label_from] = label_to





#Merge chained translations
for label_from in translations:
    label_to = translations[label_from]
    while label_to in translations:
        label_to = translations[label_to]
    translations[label_from] = label_to

trans_file = open('_3 writing_style_disagreement_strings.csv', 'w')
for label_from in translations:
    label_to = translations[label_from]
    trans_file.write(label_from+'|'+label_to+'\n')
trans_file.close()
