import re
import csv
from collections import defaultdict

output_file = '_0 1 Task_1_output.csv'

#Indicators for when a video was not displayed correctly
def video_played(no_event_text):
    no_event_text = no_event_text.lower()
    video_not_played_tags = [['restricted'],
                             ['not', 'play'],
                             ['doesn', 'play'],
                             ['didn', 'play'],
                             ['didn', 'load'],
                             ['doesn', 'load'],
                             ['not', 'load'],
                             ['not', 'exist'],
                             ['error'],
                             ['not' 'available'],
                             ['unavailable'],
                             ['nothing', 'displayed'],
                             ['no', 'video'],
                             ['video', 'exist'],
                             ['video', 'blocked'],
                             ['no','video'],
                             ['video','play'],
                             ['doesn', 'work']]
    for video_not_played_tag in video_not_played_tags:
        played = False
        for tag in video_not_played_tag:
            if not tag in no_event_text:
                played = True
                break
        if played == False:
            return False
    return True
    

def create_worker_video_annotation_file(file_name):

    if '.csv' in file_name:
        file_name = file_name.replace('.csv', '')
    result_file = open(file_name+'.csv', 'r')
    csvData = csv.reader(result_file, delimiter=',', quotechar='"')
    headers = csvData.next()
    video_url_id = headers.index('video_url')
    video_fragment_id = headers.index('fragment')
    
    #Get the correct column indexes for the useful information
    noevents_id = headers.index('noevents')
    expert_label_id = headers.index('expert_label')
    event_count_id = headers.index('eventcount')
    worker_id_id = headers.index('_worker_id')
    feedback_id = headers.index('feedback')
    
    #Up to 30 annotations are possible per line
    timerregex = 'ev\d{1,2}a'
    labelregex = 'eventlabel\d{1,2}'
    
    timerIds = {}
    labelIds = {}
    
    for i in range(0, len(headers)):
        header = headers[i]
        if re.match(timerregex, header):
            idnr = re.findall('\d{1,2}', header)
            timerIds[idnr[0]] = i
        if re.match(labelregex, header):
            idnr = re.findall('\d{1,2}', header)
            labelIds[idnr[0]] = i
    
    worker_video_annotation_file = open('_0 2 worker_annotations_per_fragment.csv','w')
    worker_video_annotation_file.write('worker_id|video_url|fragment|expert_label|event_label\n')
    #video_not_played_file = open(file_name+'_Video_not_played.csv','w')
    #video_not_played_file.write('worker_id|video_url|video_fragment|no_event_text\n')
    for row in csvData:
        worker_id = row[worker_id_id]
        video_url = row[video_url_id]
        video_fragment = row[video_fragment_id]
        noevents = row[noevents_id]
        expert_label = row[expert_label_id]
        feedback = row[feedback_id]
        events = []
        #In case the no_events checkbox was enabled, add NO_EVENT to the events labels
        if len(noevents) > 0:
            if not video_played(noevents):
                #video_not_played_file.write(worker_id+'|'+video_url+'|'+video_fragment+'|'+noevents+'\n')
                continue
            events.append('NO_EVENT')
        for i in range(0,30):
            i = str(i)
            label = row[labelIds[i]].strip().lower()
            #Check whether the event column has been annotated
            if len(label) > 0:                
                if not video_played(label):
                    #video_not_played_file.write(worker_id+'|'+video_url+'|'+video_fragment+'|'+label+'\n')
                    continue
                events.append(label)
        for event in events:
            split_event = event.split(',')
            for ev in split_event:
                ev = ev.strip()
                worker_video_annotation_file.write(worker_id+'|'+video_url+'|'+video_fragment+'|'+expert_label+'|'+ev+'\n')
    #video_not_played_file.close()
    worker_video_annotation_file.close()
    return '_0 2 worker_annotations_per_fragment.csv'

create_worker_video_annotation_file(output_file)
