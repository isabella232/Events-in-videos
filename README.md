# Crowdsourcing sample quality scores for multimedia event detection

Gathering annotated data for machine learning applications can be very time consuming and expensive. Crowdsourcing is found to be an effective method to overcome this problem. CrowdTruth is an approach for crowdsourcing that utilizes disagreement between multiple annotators to determine the quality of workers, labels and data points. In this paper, we introduce a method based on the CrowdTruth approach to effectively gather annotations for events in videos by using multiple annotators per video. We analyze the effectiveness of increasing the amount of annotators and show how multiple annotators can be used to extract information about the quality of a worker, the ambiguity of a label and finally the quality score for each video. We show how these video quality scores can be utilized by a Support Vector Machine during training to improve the performance of the classifier. We compare our own crowd sourced annotations with the crowdsourcing method of Jiang et al. 2011. Results confirm that using exclusively high-quality data points as positives examples can improve results on both accuracy and ranking metrics significantly. 

**Robert Iepsma, Theo Gevers, Zoltan Szlavik and Lora Aroyo (2016)**

*Universiteit van Amsterdam*

## Dataset files 

This repository contains all the data and code that was used to annotate consumer videos from CCV aswell as all features and labels used during training and testing of the classifiers. We distinguish two different folders 'Code' and 'Data'. The folder 'Code' contains all python files used to compute Unit-Label scores for each video using the crowdsourcing task output. The 'Data' folder contains the input and output files from all crowdsourcing tasks together with all output files produced by the python files from 'Code'.

The data and results produced by this research have been achieved by following the following steps:
 1. Gather annotations about anything happening in a video with crowdsourcing task 1 using the input file  **[Data/Task-1/_0_Task_1_input.csv](https://github.com/CrowdTruth/Events-in-videos/blob/master/Data/Task-1/_0_Task_1_input.csv)**, employing batches with a maximum size of 30 videos. 
 2. Run python code 1 to 7 from **[/Code/Task-1](https://github.com/CrowdTruth/Events-in-videos/tree/master/Code/Task-1)** to obtain the task 2 input file **[Data/Task-1/_7_Task_2_input.csv](https://github.com/CrowdTruth/Events-in-videos/blob/master/Data/Task-1/_7_Task_2_input.csv)** and the file containing the labels with the highest Unit-Label score **[Data/Task-1/_7_average_unit_label_scores.csv](https://github.com/CrowdTruth/Events-in-videos/blob/master/Data/Task-1/_7_average_unit_label_scores.csv)**. Select labels to use for task 2 using a Unit-Label score threshold based on the average and standard deviation returned by **[Code/Task-1/7. get_highest_unit_label_score.py](https://github.com/CrowdTruth/Events-in-videos/blob/master/Code/Task-1/7.%20get_highest_unit_label_score.py)** or by manually selecting all events.
 3. Gather annotations about which labels belong to which events with corwdsourcign task 2 using the generated input file **[Data/Task-1/_7_Task_2_input.csv](https://github.com/CrowdTruth/Events-in-videos/blob/master/Data/Task-1/_7_Task_2_input.csv)**. **\*\*Note that during the original research, different input files were used because at first only 380 videos were annotated. Additional resources were aquired to annotate another 516 videos in a later stage.**

 
