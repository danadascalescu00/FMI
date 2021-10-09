# Face detection with the sliding window method and histogram of oriented gradients
## About the project
The aim of the project is to implement and test a facial detection algorithm that uses the sliding window method to locate faces in images and histrogram of oriented gradients to describe the visual content of each window .
The construction of the facial detector is done in two stages:  
<ol>
  <li><b>Training: </b>training a classifier, in our case machines with vector support (SVM), based on HOG descriptors for positive examples (36x36 px windows containing faces), respectively negative (36x36 px windows containing faces). The obtained classifier will be used in the next stage. Optionally the user can set the <b><i>use_hard_mining</i></b> parameter to <i>True</i> for retraining the classifier with falsely detected patches.
  </li>
  <li><b>Testing: </b> for a test image, we try to locate all the faces, of various sizes, that appear in it. This is done by sliding a window from left to right and from top to bottom and assigning a score to each window based on the classifier learned in the previous step. Local maxims locate the faces in the image.</li>
</ol>
<br/>

## Usage
To run the Facial Detector, run the **_run_project.py_** script from *cod* directory. The following parameters can be set by the user:
  * dim_hog_celll (= 6 pixels by default);
  * threshold (= 0 by default)
  * number of positive examples (= 6713 by default)
  * number of negative examples (= 10000 by default)
  * hard_negative_mining
  * scaling_ratio - image scaling factor
<br/>

## Algorithm Overview
### 3.1 Training Phase
A classifier is trained based on a training set that contains 6713 positive examples of size 36x36 pixels and negative examples of variable size so that it can distinguish based on the visual content of a grayscale window whether or not it contains a face.  
The number of positive examples and the number of negative examples are by default 6713 and 10,000. If the user sets the **_use_flip_images_** parameter to _True_, another 6713 positive examples will be added. These examples consist of the initial dataset of positive examples which are flipped on y-axis and then darkened (the pixel intensity of each image is changed). Furthermore, by adding flipped images we ensure that the distribution of the number of negative and positive examples is balanced.  
Following the experiments performed, the linear classifier correctly separates the descriptors of positive and negative examples (assigns scores greater than 0 for all positive dataset and scores less than 0 for all negative dataset) when the cell size in pixels, **_dim_hog_cell_**, is set with the values 2, 3, 4.

<p align="center">
          <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/hog2.png" width="450">
          <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/hog3.png" width="450">
          <p align="center"> Cell size in pixels: 2x2 (dim_hog_cell) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Cell size in pixels : 3x3                                     (dim_hog_cell)
          </p>
</p>
<p align="center">
         <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/hog4.png" width="450">                                                      
         <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/hog6.jpg" width="450">
         <p align="center"> Cell size in pixels: 4x4 (dim_hog_cell) &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Cell size in pixels : 6x6 (dim_hog_cell)</p>
</p>
<p align="center"> <b>Figure 1.</b> Visualization of the training examples scores by the learned classifier </p>
<br/>

Using **hard negative mining** we get a more robust classifier, taking into account the wrong classifications we get in the training data. One of the advantages of hard negative mining is the fact that we can obtain a much higher number of false-negative detections. We can get a high value of precision and a high detection range when setting small values for the threshold parameter. Also, hard negative mining does not significantly slow down the execution of the algorithm. 

### 3.2 Testing Phase
For each test image, at each scale, a fixed-size window of 36x36 pixels is slidded from left to right and from top to bottom, and a score is assigned by the classifier trained in the previous stage. The windows in the images that have a score higher than the set threshold and are local maxima (there is no other higher score detection that overlaps with it) locate the faces.

<b>Sliding window.</b> For an image of size H x W pixels, first, it is obtained the hog descriptor associated with the image by size l x c x 36. Then for the l horizontal cells and the c vertical cells in the image, a window containing k x k cells (k = dim_window / dim_hog_cell -1) is dragged. In total there will be (l - k + 1) * (c - k + 1) windows classified. The algorithm repeats for different image resize, thus obtaining a detector that can locate faces of various sizes.

<b>Correct location of faces in test images.</b> The performance of a facial detector is measured by its ability to correctly locate faces in images. A face is located correctly if the detection returned by the detector overlaps by more than 30% (with the rectangular window annotated in the test image). The overlap between the two windows, be they f1 and f2, is calculated based on their coordinates using the formula overlap <i> (f1, f2) = intersection (f1, f2) / reunion (f1, f2) </i>.

<b>Non-maximal suppression.</b> The facial detector performance evaluation protocol penalizes overlapping detections. Only one detection (the one that covers most of the annotated example) is considered correct, the others will be considered false-positive detections. The non_maximal_suppression function removes all detections that overlap with another higher score detection.

<b>Evaluation protocol.</b> We quantify the performance of a facial detector to correctly locate faces in test images by two values:
* **accuracy**: the percentage of detections returned by the facial detector as windows containing faces.
* **recall**(=detection rate): the percentage of faces correctly located in the test images.  

We combine the two values (precision + recall) in a precision-recall graph (Figure 5). Each point on this graph represents the accuracy and recall of the facial detector obtained for all detections (ordered in ascending order by score) that exceed a certain threshold score (threshold parameter value). The entire graph is numerically quantified by the average accuracy that represents the area below the graph.  
Figure 2 illustrates the accuracy-recall graph and average accuracy = 0.85 for the CMU + MIT dataset (contains 130 images with 511 annotated faces) for the best facial detector model obtained.
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/average_precision.png">
<p align="center"><b>Figure 2. </b>Average precision of the best model obtained</p>
</p>
<br/>
<br/>

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_natalie1.jpg" width="305">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_voyager2.jpg" width="263">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_crimson.jpg" width="230">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_john.coltrane.jpg" width ="350">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_cpd.jpg" width="510">
  <br/>
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_bwolen.jpg" width="80">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_wxm.jpg" width="95">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_trekcolr.jpg">
  <p align="center"><b>Figure 3. </b>The results obtained with the best model on the CMU + MIT data set</p>
</p>
<br/>
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img1.jpg" width="308">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img2.jpg" width="308">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img3.jpg" width="308">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img4.jpg" width="230">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img5.jpg" width="230">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img6.jpg" width="230">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/FacialDetector/results/detections_img7.jpg" width="230">
  <p align="center"><b>Figure 4. </b>The results obtained with the best model on the CursVA data set</p>
</p>
<br/>
