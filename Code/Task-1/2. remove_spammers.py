import collections, re
import pickle
import gib_detect_train
import numpy as np


worker_annotations = "_1_worker_annotations_per_fragment.csv"

#Load trained gibberish model with threshold
model_data = pickle.load(open('gib_model.pki', 'rb'))
model_mat = model_data['mat']
threshold = model_data['thresh']

def count_gib(labels):
    #Count gibberish labels based on a trained model
    count = 0
    for label in labels:
        if not gib_detect_train.avg_transition_prob(label, model_mat) > threshold:
            count += 1
    return count

def count_repetition(labels):
    #Get the maximum frequency of unique labels
    counter=collections.Counter(labels)
    return max(counter.values())

def remove_spammers(file_name):
    worker_spam_metrics = {}
    spam_metrics =[]    
    if '.csv' in file_name:
        file_name = file_name.replace('.csv', '')
    annotation_file = open(file_name+'.csv', 'r')
    clean_annotation_file = open('_2_worker_annotations_per_fragment_no_spammers.csv', 'w')
    spammers_worker_id = []
    worker_annotation_labels = {}
    #Get all worker annotation labels
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
    #Calculate the ratio of gibberish and repetition for each worker
    for worker_id in worker_annotation_labels:
        labels = worker_annotation_labels[worker_id]
        gib_count = count_gib(labels)
        repetition_count = count_repetition(labels)
        spam_metrics.append([float(gib_count)/len(labels), float(repetition_count)/len(labels)])
        worker_spam_metrics[worker_id] = [float(gib_count)/len(labels), float(repetition_count)/len(labels)]
    #Calculate the thresholds for flagging spammer (avg+2*std)
    spam_metrics = np.array(spam_metrics)
    averages = np.average(spam_metrics, axis =0)
    stds = np.std(spam_metrics, axis =0)
    gibberish_threshold = averages[0]+2*stds[0]
    repetition_threshold = averages[1]+2*stds[1]
    #Flag all spammers that exceed the threshold
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
    #Write all non_spammer annotations to new file        
    annotation_file = open(file_name+'.csv', 'r')
    for line in annotation_file.readlines()[1:]:
        info = line.strip().split('|')
        worker_id = info[0]
        if not worker_id in spammers_worker_id:
            clean_annotation_file.write(line)
    #For each worker, write their spammer stats to a file for manual analysis
    spam_metric_file = open('_2_worker_spam_matrics.csv', 'w')
    for worker_id in worker_spam_metrics:
        gibberish = str(worker_spam_metrics[worker_id][0])
        repetition = str(worker_spam_metrics[worker_id][1])
        spam_metric_file.write(worker_id+'|'+gibberish+'|'+repetition+'\n')
    spam_metric_file.close()
    annotation_file.close()
    clean_annotation_file.close()
remove_spammers(worker_annotations)
