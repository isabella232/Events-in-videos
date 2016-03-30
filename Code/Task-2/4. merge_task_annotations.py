from collections import defaultdict


f_A = open('_3_A_worker_annotations_no_spammers.csv', 'r')
f_B = open('_3_B_worker_annotations_no_spammers.csv', 'r')

labels_A =  open('_2_A_label_ids.csv', 'r')
labels_B =  open('_2_B_label_ids.csv', 'r')

task_A_annotations = {}
for line in f_A.readlines()[1:]:
    info = line.strip().split('|')
    worker = info[0]
    keyword = info[1]
    annotation = info[2]
    cur_annotations = {}
    if keyword in task_A_annotations:
        cur_annotations = task_A_annotations[keyword]
    cur_count = 0
    if annotation in cur_annotations:
        cur_count = cur_annotations[annotation]
    cur_count += 1
    cur_annotations[annotation] = cur_count
    task_A_annotations[keyword] = cur_annotations
f_A.close()
        

task_B_annotations = {}
for line in f_B.readlines()[1:]:
    info = line.strip().split('|')
    worker = info[0]
    keyword = info[1]
    annotation = info[2]
    cur_annotations = {}
    if keyword in task_B_annotations:
        cur_annotations = task_B_annotations[keyword]
    cur_count = 0
    if annotation in cur_annotations:
        cur_count = cur_annotations[annotation]
    cur_count += 1
    cur_annotations[annotation] = cur_count
    task_B_annotations[keyword] = cur_annotations
f_B.close()

annotations_per_keyword = []
all_keyword_annotations = {}
for keyword in task_A_annotations:
    #print 'KEYWORD:', keyword
    annotations_A = task_A_annotations[keyword]
    annotations_B = task_B_annotations[keyword]
    none_other_count_A = 0
    if "Other category/None of the above" in annotations_A:
        none_other_count_A = annotations_A["Other category/None of the above"]
    none_other_count_B = 0
    if "Other category/None of the above" in annotations_B:
        none_other_count_B = annotations_B["Other category/None of the above"]
    total_count_A = sum(annotations_A.values())
    total_count_B = sum(annotations_B.values())
    for annotation in annotations_A:
        cur_count = annotations_A[annotation]        
        to_add = float(none_other_count_B*cur_count)/total_count_A
        if annotation == "Other category/None of the above":
            annotations_A[annotation] = to_add
        else:
            annotations_A[annotation] = cur_count+to_add
    for annotation in annotations_B:
        cur_count = annotations_B[annotation]
        to_add = float(none_other_count_A*cur_count)/total_count_B
        if annotation == "Other category/None of the above":
            annotations_B[annotation] = to_add
        else:
            annotations_B[annotation] = cur_count+to_add
    total_annotations = defaultdict(float)
    for annotation in annotations_A:
        total_annotations[annotation] += annotations_A[annotation]
    for annotation in annotations_B:
        total_annotations[annotation] += annotations_B[annotation]
    all_keyword_annotations[keyword] = total_annotations
    annotations_per_keyword.append(sum(total_annotations.values()))


high_cosine_labels = []

for line in labels_A.readlines():
    info = line.strip().split('|')
    label = info[0]
    if not label in high_cosine_labels:
        high_cosine_labels.append(label)
labels_A.close()
for line in labels_B.readlines():
    info = line.strip().split('|')
    label = info[0]
    if not label in high_cosine_labels:
        high_cosine_labels.append(label)
labels_B.close()

labelf = open('_4_categoryNames.csv', 'w')
for high_cos_label in high_cosine_labels:
    labelf.write(high_cos_label+'\n')
labelf.close()

keywordf = open('_4_units.csv', 'w')
labelf = open('_4_merged_unit_vectors.csv', 'w')
for keyword in all_keyword_annotations:
    annotations = all_keyword_annotations[keyword]
    keywordf.write(keyword+'\n')
    labels = []
    for high_cos_label in high_cosine_labels:
        labels.append(annotations[high_cos_label])
    labels = [str(l) for l in labels]
    labelf.write(' '.join(labels)+'\n')
keywordf.close()
labelf.close()
