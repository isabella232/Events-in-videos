import numpy as np
from collections import defaultdict
label_name = '_1_keyword_labels_binary'
lf = open(label_name+'.csv', 'r')
labels = []
for line in lf.readlines():
    info = line.strip().split(' ')
    info = [float(i) for i in info]
    labels.append(info)
lf.close()

labels = np.array(labels)

nr_keywords, nr_labels = labels.shape

label_occurences = [0 for i in range(0, nr_labels)]
label_co_occurences = defaultdict(int)
label_not_co_occurences = defaultdict(int)

for i in range(0, nr_keywords):
    keyword_labels = labels[i]
    occurences = []
    for A in range(0, nr_labels):
        A_count = keyword_labels[A]
        if keyword_labels[A] > 0:
            label_occurences[A] += 1
        for B in range(0, nr_labels):
            B_count = keyword_labels[B]
            key = str(A)+'_'+str(B)
            if A_count > 0 and B_count > 0:
                label_co_occurences[key] += 1
            if A_count == 0 and B_count > 0:
                label_not_co_occurences[key] += 1

f = open('_2_label_similarities.csv', 'w')
for A in range(0, nr_labels):
    sims = []
    for B in range(0, nr_labels):
        key = str(A)+'_'+str(B)
        numOccurences_A = label_occurences[A]
        numOccurences_not_A = nr_keywords - numOccurences_A
        P_B_given_A = float(label_co_occurences[key])/numOccurences_A
        P_B_given_not_A = float(label_not_co_occurences[key])/numOccurences_not_A
        similarity = (P_B_given_A-P_B_given_not_A)/(1-P_B_given_not_A)
        if similarity < 0.0:
            similarity = 0.0
        sims.append(str(similarity))
    f.write(' '.join(sims)+'\n')
f.close()        



    
