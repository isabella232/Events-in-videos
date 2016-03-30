import Metrics
from collections import defaultdict
import collections

filetype = 'B'
#filetype = 'CCV_clustering_keywords_2_ALL'
#filetype = 'Cluster1_ALL'
#filetype = 'Cluster2_ALL'
worker_label_vectors_file = open('_2_'+filetype+'_worker_vectors.csv', 'r')
annotation_file = open('_1_'+filetype+'_worker_annotations.csv', 'r')
spammer_file = open('_3_'+filetype+'_worker_spam_metrics.csv', 'w')
label_id_file = open('_2_'+filetype+'_label_ids.csv', 'r')

no_spammers_file = open('_3_'+filetype+'_worker_annotations_no_spammers.csv', 'w')
annotation_file_2 = open('_1_'+filetype+'_worker_annotations.csv', 'r')

high_cosine_labels = []
for line in label_id_file.readlines():
    label = line.strip().split('|')[0]
    if not label == 'Other category/None of the above':
        high_cosine_labels.append(label)

worker_dict = {}
for line in worker_label_vectors_file.readlines():
    info = line.strip().split('|')
    worker_id = info[0]
    label = info[1]
    vector = info[2:]
    vector = [int(i) for i in vector]
    if worker_id in worker_dict:
        cur_label_vectors = worker_dict[worker_id]
    else:
        cur_label_vectors = {}
    cur_label_vectors[label] = vector
    worker_dict[worker_id] = cur_label_vectors
worker_label_vectors_file.close()

#worker_agreement  
worker_agreement_dict = Metrics.get_worker_agreement(worker_dict)

#avg_worker_sentence_score
avg_worker_sentence_agreement_dict = Metrics.get_avg_worker_sentence_agreement(worker_dict)

#Avg Amount of annotations per label
avg_worker_annotations = {}
for worker in worker_dict:
    total_annotations = 0
    labels = worker_dict[worker]
    for label in labels:
        vector = labels[label]
        total_annotations += sum(vector)
    avg_annotations = float(total_annotations)/len(labels)
    avg_worker_annotations[worker] = avg_annotations
    

worker_annotations = {}
for line in annotation_file.readlines():
    info = line.strip().split('|')
    worker = info[0]
    label = info[1]
    annotation = info[2]
    cur_worker_labels = {}
    if worker in worker_annotations:
        cur_worker_labels = worker_annotations[worker]
    cur_label_annotations = []
    if label in cur_worker_labels:
        cur_label_annotations = cur_worker_labels[label]
    cur_label_annotations.append(annotation)
    cur_worker_labels[label] = cur_label_annotations
    worker_annotations[worker] = cur_worker_labels
annotation_file.close()    

def count_repetition(labels):
    counter=collections.Counter(labels)
    return max(counter.values())

worker_repetition_measure = {}
worker_high_cosine_fail_counts = {}
for worker in worker_annotations:
    all_worker_annotations = []
    cur_worker_labels = {}
    if worker in worker_annotations:
        cur_worker_labels = worker_annotations[worker]
    for label in cur_worker_labels:
        annotations = cur_worker_labels[label]
        in_label = []
        for high_cosine_label in high_cosine_labels:
            if high_cosine_label.lower() in label.lower().split(' '):
                in_label.append(high_cosine_label.lower())
        in_annotation = []
        for annotation in annotations:
            all_worker_annotations.append(annotation)
            if annotation.lower() in label.lower().split(' '):
                in_annotation.append(annotation.lower())
        worker_high_cosine_fail = []
        if worker in worker_high_cosine_fail_counts:
            worker_high_cosine_fail = worker_high_cosine_fail_counts[worker]
        for lab in in_label:
            if not lab in in_annotation:
                worker_high_cosine_fail.append(1)
            else:
                worker_high_cosine_fail.append(0)
        worker_high_cosine_fail_counts[worker] = worker_high_cosine_fail
    repetitions = count_repetition(all_worker_annotations)
    worker_repetition_measure[worker] = float(repetitions)/len(all_worker_annotations)
        
worker_high_cosine_fails = {}
for worker in worker_high_cosine_fail_counts:
    fail_counts = worker_high_cosine_fail_counts[worker]
    if len(fail_counts) > 0:
        high_cosine_fails = float(sum(fail_counts))/len(fail_counts)
    else:
        high_cosine_fails = 0
    worker_high_cosine_fails[worker] = high_cosine_fails

spammer_file.write('worker_id|worker_agreement|avg_worker_sentence_agreement|avg_annotation_count|high_cosine_fails\n')
for worker in worker_agreement_dict:
    worker_agreement = str(worker_agreement_dict[worker])
    worker_sentence_agreement = str(avg_worker_sentence_agreement_dict[worker])
    avg_annotation_count = str(avg_worker_annotations[worker])
    high_cosine_fails = str(worker_high_cosine_fails[worker])
    spammer_file.write(worker+'|'+worker_agreement+'|'+worker_sentence_agreement+'|'+avg_annotation_count+'|'+high_cosine_fails+'\n')
spammer_file.close()

import numpy
worker_agreement_list = numpy.array(worker_agreement_dict.values())
avg_worker_sentence_agreement_list = numpy.array(avg_worker_sentence_agreement_dict.values())
avg_worker_annotations_list = numpy.array(avg_worker_annotations.values())
worker_high_cosine_fails_list = numpy.array(worker_high_cosine_fails.values())
worker_repetition_list = numpy.array(worker_repetition_measure.values())
wa_avg = numpy.average(worker_agreement_list)
wa_std = worker_agreement_list.std()
ws_avg = numpy.average(avg_worker_sentence_agreement_list)
ws_std = avg_worker_sentence_agreement_list.std()
avg_avg = numpy.average(avg_worker_annotations_list)
avg_std = avg_worker_annotations_list.std()
cos_avg = numpy.average(worker_high_cosine_fails_list)
cos_std = worker_high_cosine_fails_list.std()
rep_avg = numpy.average(worker_repetition_list)
rep_std = worker_repetition_list.std()
print 'Worker_agreement avg std:', numpy.average(worker_agreement_list), worker_agreement_list.std()
print 'Worker_sentence_agreement avg std:', numpy.average(avg_worker_sentence_agreement_list), avg_worker_sentence_agreement_list.std()
print 'Avg_annotation_count avg std:', numpy.average(avg_worker_annotations_list), avg_worker_annotations_list.std()
print 'Worker_high_cosine_fails avg std:', numpy.average(worker_high_cosine_fails_list), worker_high_cosine_fails_list.std()
print 'Worker_repetition avg std:', rep_avg, rep_std
#import plotdistributions
#plotdistributions.plot_distributions(sorted(worker_high_cosine_fails.values()),'')

spammers = []
     
for worker in worker_agreement_dict:
    worker_agreement = worker_agreement_dict[worker]
    worker_sentence_agreement = avg_worker_sentence_agreement_dict[worker]
    avg_annotation_count = avg_worker_annotations[worker]
    high_cosine_fails = worker_high_cosine_fails[worker]
    repetition = worker_repetition_measure[worker]
    failed = ''
    fails = 0
    if worker_agreement < wa_avg - wa_std:
        fails += 1
        failed += ' Workeragreement: '+str(worker_agreement)
    if worker_sentence_agreement < ws_avg - ws_std:
        fails += 1
        failed += ' Workersentence: '+str(worker_sentence_agreement)
    if avg_annotation_count > avg_avg + avg_std:
        fails += 0
        failed += ' Averageannotations: '+str(avg_annotation_count)
    if high_cosine_fails > cos_avg + cos_std:
        fails += 1
        failed += ' Cosfails: '+str(high_cosine_fails)
    if repetition > rep_avg + rep_std:
        fails += 1
        failed += ' Repetition: '+str(repetition)
    if fails >= 3:
        spammers.append(worker)
        print worker
        #print '\t', fails
        #print '\t', failed


for line in annotation_file_2.readlines():
    info = line.strip().split('|')
    worker = info[0]
    if not worker in spammers:
        no_spammers_file.write(line)
annotation_file_2.close()  
no_spammers_file.close()
