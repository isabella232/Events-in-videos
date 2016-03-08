trans_file = open('_3 writing_style_disagreement_strings.csv', 'r')
trans_1 = {}
for line in trans_file.readlines():
    info = line.strip().split('|')
    label_from = info[0]
    label_to = info[1]
    trans[label_from] = label_to
trans_file.close()

trans_file = open('_4 writing_style_disagreement_wordnet.csv', 'r')
trans_2 = {}
for line in trans_file.readlines():
    info = line.strip().split('|')
    label_from = info[0]
    label_to = info[1]
    trans_2[label_from] = label_to
trans_2.close()


f = open('_1 0 worker_annotations_per_fragment_no_spammers.csv', 'r')
f2 = open('_5 worker_annotations_per_fragment_no_spammers_no_writing_style_disagreement.csv', 'w')
for line in f.readlines():
    info = line.strip().split('|')
    label = info[3]
    if label in trans_1:
        label = trans_1[label]
    if label in trans_2:
        label = trans_2[label]
    info[3] = label
    f2.write('|'.join(info)+'\n')
f.close()
f2.close()
