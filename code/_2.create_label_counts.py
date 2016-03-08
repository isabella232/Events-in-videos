from collections import defaultdict

label_counts = defaultdict(int)

f = open('_1 0 worker_annotations_per_fragment_no_spammers.csv', 'r')
for line in f.readlines():
    info  = line.strip().split('|')
    label = info[4]
    label_counts[label] += 1
f.close()

labelcountfile = open('_2 label_counts.csv', 'w')
for label in label_counts:
    labelcountfile.write(label+'|'+str(label_counts[label])+'\n')
labelcountfile.close()
