from nltk.corpus import wordnet as wn
from collections import defaultdict
from itertools import product

translation_file = '_3 writing_style_disagreement.csv'
labelcounts_file = '_2 label_counts.csv'

writing_style_translations = {}
f = open(translation_file, 'r')
for line in f.readlines():
    info = line.strip().split('|')
    writing_style_translations[info[0]] = info[1]
f.close()

all_label_counts = defaultdict(int)
f = open(labelcounts_file, 'r')
for line in f.readlines():
    info = line.strip().split('|')
    label = info[0]
    count = float(info[1])
    if label in writing_style_translations:
        label = writing_style_translations[label]
    all_label_counts[label] += count
f.close()


def wordnet_equal(label_1, label_2):
    words_1 = list(set(label_1.split(' ')))
    words_2 = list(set(label_2.split(' ')))
    if not len(words_1) == len(words_2):
        return False
    total_sim = 0
    for i in range(0, len(words_1)):        
        word_1 = words_1[i]
        word_2 = words_2[i]
        ss1 = wn.synsets(word_1)
        ss2 = wn.synsets(word_2)
        prod = product(ss1, ss2)        
        if len(list(prod)) > 1:
            word_max = max(s1.path_similarity(s2) for (s1, s2) in product(ss1, ss2))
            total_sim += word_max
    total_sim = float(total_sim)/len(words_1)
    if total_sim >= 1.0:
        print word_1, word_2, total_sim, list(prod)
        return True
    return False

translations = {}

all_labels = all_label_counts.keys()
for i in range(0, len(all_labels)-1):
    print i
    for j in range(i+1, len(all_labels)):
        label_1 = all_labels[i]
        label_2 = all_labels[j]
        label_1_count = all_label_counts[label_1]
        label_2_count = all_label_counts[label_2]
        try:
            equal = wordnet_equal(label_1, label_2)
        except:
            equal = False
        if equal:
            if label_1_count > label_2_count:
                translations[label_1] = label_2
            else:
                translations[label_2] = label_1
            break
             
for label_from in translations:
    label_to = translations[label_from]
    while label_to in translations:
        label_to = translations[label_to]
    translations[label_from] = label_to

f = open('_4 writing_style_disagreement_similarity.csv','w')
for label_from in translations:
    label_to = translations[label_from]
    f.write(label_from+'|'+label_to+'\n')
f.close()
