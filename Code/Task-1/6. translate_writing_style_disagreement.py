trans_file = open('_4_writing_style_disagreement_strings.csv', 'r')
trans_1 = {}
for line in trans_file.readlines():
    info = line.strip().split('|')
    label_from = info[0]
    label_to = info[1]
    trans_1[label_from] = label_to
trans_file.close()

trans_file = open('_5_writing_style_disagreement_wordnet.csv', 'r')
trans_2 = {}
for line in trans_file.readlines():
    info = line.strip().split('|')
    label_from = info[0]
    label_to = info[1]
    trans_2[label_from] = label_to
trans_file.close()


f = open('_2_worker_annotations_per_fragment_no_spammers.csv', 'r')
f2 = open('_6_worker_annotations_per_fragment_no_spammers_no_writing_style_disagreement.csv', 'w')
for line in f.readlines():
    info = line.strip().split('|')
    label = info[4]
    if label in trans_1:
        label = trans_1[label]
    if label in trans_2:
        label = trans_2[label]
    info[4] = label
    f2.write('|'.join(info)+'\n')
f.close()
f2.close()
