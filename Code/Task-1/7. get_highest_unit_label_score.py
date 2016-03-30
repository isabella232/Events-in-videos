from collections import Counter
import operator
import scipy.spatial
annotation_file = open('_6_worker_annotations_per_fragment_no_spammers_no_writing_style_disagreement.csv', 'r')

avg_video_event_cosines = {}
annotation_video_event_cosines = {}
video_annotations = {}
for line in annotation_file.readlines():
    info = line.strip().split('|')
    video = info[1]
    annotation = info[4]
    if video in video_annotations:
        cur_video_annotations = video_annotations[video]
    else:
        cur_video_annotations = []
    cur_video_annotations.append(annotation)
    video_annotations[video] = cur_video_annotations

for video in video_annotations:
    annotations = video_annotations[video]
    c = Counter( annotations )
    all_annotations_vector = []
    vector_id_annotations = []
    for annotation in c:
        count = int(c[annotation])
        all_annotations_vector.append(count)
        vector_id_annotations.append(annotation)

    for i in range(0, len(vector_id_annotations)):
        annotation = vector_id_annotations[i]
        cur_annotation_vector = [0 for j in range(0, len(all_annotations_vector))]
        cur_annotation_vector[i] = 1
        video_event_cosine = 1.0-scipy.spatial.distance.cosine(cur_annotation_vector,all_annotations_vector)
        if annotation in annotation_video_event_cosines:
            cur_annotation_video_event_cosines = annotation_video_event_cosines[annotation]
        else:
            cur_annotation_video_event_cosines = []
        cur_annotation_video_event_cosines.append(float(video_event_cosine))
        annotation_video_event_cosines[annotation] = cur_annotation_video_event_cosines
    
for annotation in annotation_video_event_cosines:
    video_event_cosines = annotation_video_event_cosines[annotation]
    avg_video_event_cosine = sum(video_event_cosines) / float(len(video_event_cosines))
    avg_video_event_cosines[annotation] = avg_video_event_cosine


label_cos_file = open('_7_average_unit_label_scores.csv', 'w')
label_for_task_file = open('_7_Task_2_input.csv', 'w')
sorted_avg_annotation_frequencies = sorted(avg_video_event_cosines.items(), key=operator.itemgetter(1), reverse=True)
all_cosines = []
for i in range(0, len(sorted_avg_annotation_frequencies)):
    str_info = [str(j) for j in sorted_avg_annotation_frequencies[i]]
    label_cos_file.write(str_info[0]+'|'+str(1*float(str_info[1]))+'\n')
    label_for_task_file.write(str(i)+'|'+str_info[0]+'\n')
    all_cosines.append(float(str_info[1]))
label_cos_file.close()
label_for_task_file.close()

import numpy as np
np_all_cosines = np.array(all_cosines)
avg = np.average(np_all_cosines)
std = np.std(np_all_cosines)
print avg, std
print avg+3*std

for i in range(0, 50):
    print sorted_avg_annotation_frequencies[i] 



