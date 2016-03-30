refinement_type = '_1_A_worker_annotations'
worker_video_annotation_file_name = refinement_type+'.csv'

spammer = []

worker_video_annotation_file = open(worker_video_annotation_file_name, 'r')
label_ids = {}
for line in worker_video_annotation_file.readlines()[1:]:
    info = line.strip().split('|')
    annotation = info[2]
    if not annotation in label_ids:
        label_ids[annotation] = len(label_ids)
worker_video_annotation_file.close()

#Write the label_ids to a file for later analysis to remember label->id
labels_ids_file = open('_2_'+refinement_type[3]+'_label_ids.csv','w')
for label in label_ids:
    labels_ids_file.write(label+'|'+str(label_ids[label])+'\n')
labels_ids_file.close()


worker_video_vectors = {}
worker_video_annotation_file = open(worker_video_annotation_file_name, 'r')
for line in worker_video_annotation_file.readlines()[1:]:
    info = line.strip().split('|')
    worker_id = info[0]
    video_id = info[1]
    label = info[2]
    label_id = label_ids[label]
    if not worker_id in spammer:
        #Fill worker video vector
        if worker_id in worker_video_vectors:
            worker_videos = worker_video_vectors[worker_id]
        else:
            worker_videos = {}
        if video_id in worker_videos:
            video_vector = worker_videos[video_id]
        else:
            video_vector = [0 for i in range(0, len(label_ids))]
        video_vector[label_id] += 1
        worker_videos[video_id] = video_vector
        worker_video_vectors[worker_id] = worker_videos
worker_video_annotation_file.close()


sentence_vectors = {}
worker_video_vector_file = open('_2_'+refinement_type[3]+'_worker_vectors.csv', 'w')
for worker in worker_video_vectors:
    worker_videos = worker_video_vectors[worker]
    for video in worker_videos:
        worker_video_vector = worker_videos[video]
        if video in sentence_vectors:
            cur_sentence_vectors = sentence_vectors[video]
        else:
            cur_sentence_vectors = [0 for i in range(len(label_ids))]
        cur_sentence_vectors = [cur_sentence_vectors[i] + worker_video_vector[i] for i in range(0, len(worker_video_vector))]
        sentence_vectors[video] = cur_sentence_vectors
        worker_video_vector_file.write(worker+'|'+video+'|'+'|'.join([str(i) for i in worker_video_vector])+'\n')
worker_video_vector_file.close()

video_vector_file = open('_2_'+refinement_type[3]+'_unit_vectors.csv', 'w')
for video in sentence_vectors:
    total_vector = sentence_vectors[video]
    video_vector_file.write(video+'|'+'|'.join([str(i) for i in total_vector])+'\n')
video_vector_file.close()   
