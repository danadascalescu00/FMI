# Face detection with the sliding window method and histogram of oriented gradients
## About the project
The aim of the project is to implement and test a facial detection algorithm that uses the sliding window method to locate faces in images and histrogram of oriented gradients to describe the visual content of each window .
The construction of the facial detector is done in two stages:  
<ol>
  <li><b>Training</b> Training a classifier, in our case machines with vector support (SVM), based on HOG descriptors for positive examples (36x36 px windows containing faces), respectively negative (36x36 px windows containing faces). The obtained classifier will be used in the next stage. Optionally the user can set the use_hard_mining parameter to True for retraining the classifier with falsely detected patches.
  </li>
  <li><b>Testing</b></li>
</ol>

## Algorithm Overview
