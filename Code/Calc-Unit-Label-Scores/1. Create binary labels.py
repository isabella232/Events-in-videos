import numpy as np
f = open('_0_ACTUALUSED_keyword_labels.csv', 'r')
label_annotations = []
for line in f.readlines():
    annotations = line.strip().split(' ')
    label_annotations.append(annotations)
f.close()

label_annotations = np.array(label_annotations).astype(float)

no_zero_means = []
for i in range(0, 32):
    non_zero = []
    annotations = label_annotations[:,i]
    for annotation in annotations:
        if annotation > 0:
            non_zero.append(annotation)
    no_zero_means.append(np.average(non_zero))
print 


averages = np.average(label_annotations, axis=0)
stds = np.average(label_annotations, axis=0)
print averages

averages = no_zero_means

f = open('_1_keyword_labels_binary.csv','w')
for annotations in label_annotations:
    binary_annotations = []
    for i in range(0, len(annotations)):
        val = annotations[i]
        mean = averages[i]
        if val >= mean:
            val = '1'
        else:
            val = '0'
        binary_annotations.append(val)
    
    f.write(' '.join(binary_annotations)+'\n')
f.close()
        
