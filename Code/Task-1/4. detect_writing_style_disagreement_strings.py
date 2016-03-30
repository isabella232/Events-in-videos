import re, collections
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity 


label_count_file = '_3_label_counts.csv'

stop = stopwords.words('english')
stemmer = PorterStemmer()

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

trans_file = open('_4_writing_style_disagreement_strings.csv', 'w')
for label_from in translations:
    label_to = translations[label_from]
    trans_file.write(label_from+'|'+label_to+'\n')
trans_file.close()
