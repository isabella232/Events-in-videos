import scipy.spatial

def get_cur_label_count(cur_label, labels, similarities):
    cur_count = 0
    #print cur_label
    for i in range(0, len(labels)):
        #print i, similarities[str(cur_label)+'_'+str(i)], labels[i]
        cur_count += similarities[str(cur_label)+'_'+str(i)]*labels[i]
        #print cur_count
    return cur_count


category_file = open('_0_ACTUALUSED_categoryNames.csv', 'r')
othernone_id = 0
total_cats = 0
for line in category_file.readlines():
    name = line.strip()
    if name == 'Other category/None of the above':
        othernone_id = total_cats
    total_cats += 1

print othernone_id

similarities = {}
f = open('_2_label_similarities.csv', 'r')
sims = f.readlines()
for i in range(0, len(sims)):
    line = sims[i]
    vals = line.strip().split(' ')
    for j in range(0, len(vals)):
        if i == othernone_id and j == othernone_id:
            val = vals[j]
        elif i == othernone_id or j == othernone_id:#Do not use Other/None in similarities
            val = 0.0
        else:
            val = vals[j]
        similarities[str(i)+'_'+str(j)] = float(val)
f.close()  

#Parade = 3
#Graduation = 5
#Birthday = 8
#usefull_is = [Parade,Graduation,Birthday]
usefull_is = [i for i in range(total_cats)]
print usefull_is
    
f = open('_0_video_labels.csv', 'r')
f2 = open('_3_unit_label_scores.csv', 'w')
for line in f.readlines()[0:]:
    info = line.strip().split(' ')
    labels = [float(i) for i in info]
    #print labels
    label_scores = []
    for i in usefull_is:
        new_labels = list(labels)
        new_labels[i] = get_cur_label_count(i, labels, similarities)
        for j in range(0, i):
            new_labels[j] = (1-similarities[str(i)+'_'+str(j)])*labels[j]
        for j in range(i+1,len(labels)):
            new_labels[j] = (1-similarities[str(i)+'_'+str(j)])*labels[j]
        for j in range(0, len(labels)):
            if new_labels[j] < 0:
                new_labels[j] = 0.0
        cur_vector = [0 for j in range(0, len(new_labels))]
        cur_vector[i] = 1
        #print 'CURLABEL: ', i
        #print new_labels
        #new_labels = list(labels) # USE THIS TO NOT USE SIMILARITIES
        label_score = 1.0-scipy.spatial.distance.cosine(cur_vector,new_labels)
        label_scores.append(label_score)
    # labels
    #print label_scores    
    #print label_scores
    #break
    for i in range(total_cats):
        f2.write("{0:.2f} ".format(label_scores[i]))
    f2.write("\n")
f2.close()
f.close()

