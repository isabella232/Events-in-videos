import collections, re
import pickle
import gib_detect_train
import numpy as np


worker_annotations = "_0 2 worker_annotations_per_fragment.csv"

model_data = pickle.load(open('gib_model.pki', 'rb'))
model_mat = model_data['mat']
threshold = model_data['thresh']

def count_gib(labels):
    count = 0
    for label in labels:
        if not gib_detect_train.avg_transition_prob(label, model_mat) > threshold:
            count += 1
    return count

def count_special(labels):
    count = 0
    regex = re.compile('[a-zA-Z0-9 \.\'\"\,\-\_]')
    for label in labels:
        specials = regex.sub('', label)
        if len(specials) > 0:
            count += 1
    return count  

def count_repetition(labels):
    counter=collections.Counter(labels)
    return max(counter.values())

def remove_spammers(file_name):
    worker_spam_metrics = {}
    spam_metrics =[]
    '''
        Input : file_name
        Output: file_name
        Based on labels only, high repetition, high count none-sense words
        > 18% gibberish
        > 100% special characters
        > 47% repetition        
    '''
    
    if '.csv' in file_name:
        file_name = file_name.replace('.csv', '')
    annotation_file = open(file_name+'.csv', 'r')
    clean_annotation_file = open('_1 0 worker_annotations_per_fragment_no_spammers.csv', 'w')
    #spammer_file = open(file_name+'_spammers.csv', 'w')
    spammers_worker_id = []
    worker_annotation_labels = {}
    for line in annotation_file.readlines()[1:]:
        info = line.strip().split('|')
        worker_id = info[0]
        event_label = info[4]
        if worker_id in worker_annotation_labels:
            current_labels = worker_annotation_labels[worker_id]
        else:
            current_labels = []
        current_labels.append(event_label)
        worker_annotation_labels[worker_id] = current_labels
    annotation_file.close()
    for worker_id in worker_annotation_labels:
        labels = worker_annotation_labels[worker_id]
        gib_count = count_gib(labels)
        special_char_count = count_special(labels)
        repetition_count = count_repetition(labels)
        spam_metrics.append([float(gib_count)/len(labels), float(repetition_count)/len(labels)])
        worker_spam_metrics[worker_id] = [float(gib_count)/len(labels), float(repetition_count)/len(labels)]
    spam_metrics = np.array(spam_metrics)
    averages = np.average(spam_metrics, axis =0)
    stds = np.std(spam_metrics, axis =0)
    gibberish_threshold = averages[0]+2*stds[0]
    repetition_threshold = averages[1]+2*stds[1]
    for worker_id in worker_spam_metrics:
        labels = worker_annotation_labels[worker_id]
        gib_count = worker_spam_metrics[worker_id][0]
        repetition_count = worker_spam_metrics[worker_id][1]
        if float(gib_count) > gibberish_threshold:
            print 'SPAMMER: ', worker_id, 'GIBBERISH', float(gib_count), len(labels), float(gib_count)/len(labels)
            spammers_worker_id.append(worker_id)
        elif float(repetition_count) > repetition_threshold and len(labels) > 10:
            print 'SPAMMER: ', worker_id, 'REPITITION', float(repetition_count), len(labels), float(repetition_count)/len(labels)
            spammers_worker_id.append(worker_id)
        if len(labels) <=10:
            repetition_count = 0
    
        
    annotation_file = open(file_name+'.csv', 'r')
    for line in annotation_file.readlines()[1:]:
        info = line.strip().split('|')
        worker_id = info[0]
        if not worker_id in spammers_worker_id:
            clean_annotation_file.write(line)
        else:
            #spammer_file.write(line)
            continue
    spam_metric_file = open('_1 1 worker_spam_matrics.csv', 'w')
    for worker_id in worker_spam_metrics:
        gibberish = str(worker_spam_metrics[worker_id][0])
        repetition = str(worker_spam_metrics[worker_id][1])
        spam_metric_file.write(worker_id+'|'+gibberish+'|'+repetition+'\n')
    spam_metric_file.close()
    annotation_file.close()
    clean_annotation_file.close()
    #spammer_file.close()
    return '_1 0 worker_annotations_per_fragment_no_spammers.csv'
remove_spammers(worker_annotations)
