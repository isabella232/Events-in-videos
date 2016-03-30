import re
import csv
    

output_file = '_0_Task_2_B_output.csv'

def create_worker_video_annotation_file(file_name):
    if '.csv' in file_name:
        file_name = file_name.replace('.csv', '')
    result_file = open(file_name+'.csv', 'r')
    csvData = csv.reader(result_file, delimiter=',', quotechar='"')
    headers = csvData.next()
    worker_id_id = headers.index('_worker_id')
    label_id = headers.index('label')
    annotations_id = headers.index('to_which_category_does_this_label_belong_multiple_selections_possible')
    #url_id = headers.index('url')

    worker_video_annotation_file = open('_1_'+file_name[10]+'_worker_annotations.csv','w')
    worker_video_annotation_file.write('worker_id|label|annotation\n')
    cur_row = 0
    for row in csvData:
        cur_row += 1
        if cur_row == 1:
            continue
        worker_id = row[worker_id_id]
        label = row[label_id]
        annotations = row[annotations_id].split('\n')
        #url = row[url_id]
        for annotation in annotations:
            worker_video_annotation_file.write(worker_id+'|'+label+'|'+annotation.strip()+'\n')
    worker_video_annotation_file.close()

create_worker_video_annotation_file(output_file)
