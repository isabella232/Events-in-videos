# Events in videos

Crowdsourcing sample quality scores for multimedia event detection

Gathering annotated data for machine learning applications can be very time consuming and expensive. Crowdsourcing is found to be an effective method to overcome this problem. CrowdTruth is an approach for crowdsourcing that utilizes disagreement between multiple annotators to determine the quality of workers, labels and data points. In this paper, we introduce a method based on the CrowdTruth approach to effectively gather annotations for events in videos by using multiple annotators per video. We analyze the effectiveness of increasing the amount of annotators and show how multiple annotators can be used to extract information about the quality of a worker, the ambiguity of a label and finally the quality score for each video. We show how these video quality scores can be utilized by a Support Vector Machine during training to improve the performance of the classifier. We compare our own crowd sourced annotations with the crowdsourcing method of Jiang et al. 2011. Results confirm that using exclusively high-quality data points as positives examples can improve results on both accuracy and ranking metrics significantly. 
**Robert Iepsma, Theo Gevers, Zoltan Szlavik and Lora Aroyo (2016)**

*Universiteit van Amsterdam*


This repository contains all the data and code that was used to annotate consumer videos from CCV aswell as all features and labels used during training and testing of the classifiers.
