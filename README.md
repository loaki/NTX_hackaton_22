# INS: Immersive Neuro Simulation

## About / Synopsis

* Problematic: How to create an immersive world by linking computer interface and human biosignals.
* Prototype

## Process

* EEG sensors with Bitalino
* Data acquisition and processing with Timeflux

![emg_eeg](/assets/emg_eeg_right_eye.png)

* Labeling dataset for assets (left, right, rest) ~60 records each 
* Training classification model with sklearn SVC

![svm_report](/assets/svm_report.png)

* Recognize eye movements in real time to interact in game

![img1](/assets/img1.jpg)
![img2](/assets/img2.jpg)

## Resources (Documentation and other links)

https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

https://github.com/timeflux
