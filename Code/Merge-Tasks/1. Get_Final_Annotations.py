from collections import defaultdict
f = open('_0_ACTUALUSED_video_worker_annotations.csv', 'r')
video_keywords = defaultdict(list)
for line in f.readlines():
    info = line.strip().split('|')
    video = info[1]
    keyword = info[3].lower()#CAN ALSO BE 4 IF THE FRAGMENT IS AVAILABLE
    video_keywords[video].append(keyword.replace('"', ''))
f.close()

keyword_labels = {}
f1 = open('_0_ACTUALUSED_keywords.csv', 'r')
f2 = open('_0_ACTUALUSED_keyword_labels.csv', 'r')
keywords = f1.readlines()
labels = f2.readlines()
for i in range(0, len(keywords)):
    keyword = keywords[i].strip().lower()
    label = [float(i) for i in labels[i].strip().split(' ')]
    keyword_labels[keyword] = label
f1.close()
f2.close()

all_video_labels = {}
for video in video_keywords:
    all_labels = [0 for i in range(0,32)]
    keywords = video_keywords[video]
    for keyword in keywords:
        labels = keyword_labels[keyword]
        all_labels = [all_labels[i]+labels[i] for i in range(0, len(labels))]
    all_video_labels[video] = all_labels

f = open('_1_video_urls.csv', 'w')
f2 = open('_1_video_labels.csv', 'w')
f3 = open('_1_video_labels_uniform.csv', 'w')
for video in all_video_labels:
    labels = all_video_labels[video]
    max_label = max(labels)
    uniform_labels = ["{0:.2f}".format(i/max_label) for i in labels]
    labels = [str(i) for i in labels] 
    f.write(video+'\n')
    f2.write(' '.join(labels)+'\n')
    f3.write(' '.join(uniform_labels)+'\n')
f.close()
f2.close()
f3.close()
            
