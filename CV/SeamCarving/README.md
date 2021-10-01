# Seam Carving for Content Aware Image Resizing
The aim of the project is to resize the image while preserving the content. The technique described below is an implementation of the algorithm proposed by S.Avidan and A.Shamir in the article "Seam Carving for Content-Aware Image Resizing".
<br/>

## Usage
The **run_project.py** script sets the image to be resized and the parameters used. This script calls the _resize_image_ function, which in turn calls functions for shrinking the width or height of the image, enlarging the content, or removing an object.

## Algorithm Overview
**The basic idea:** To reduce/enlarge a size, remove/add irregular paths of pixels that connect the extremities. This operation is performed without visibly affecting the image.  
&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&ensp; We measure the 'cost of a seam' as the sum of the magnitudes of the gradients of the pixels that make up the seam. At each iteration, we choose the seam with the lowest cost in the image. We measure the 'cost of a path' as the sum of the magnitudes of the gradients of the pixels that make up the path. Dynamic programming is used to calculate the optimal path efficiently.
### Decrease the image width
The width reduction operation of an image is performed using the decrease_width function. This function removes pixels from the vertical irregular paths chosen according to the user's option:
  1. random (Figure 1)
  2. using the Greedy method (Figure 2)
  3. using the dynamic programming method (Figure 3)

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/fig_castel_width_50px_aleator.png">
  <b>Figure 1.</b> Reduce the width of the image by 50 pixels using the Greedy method
</p>

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/fig_castel_greedy_vertical.png">
  <b>Figure 2.</b> Reduce the width of the image by 50 pixels using the Greedy method
</p>

It can be observed that an algorithm based on the Greedy method does not lead to the desired results. This is due to the fact that at each step the best local solution is chosen (the pixels with the lowest gradient on the respective line are chosen), and the combination of local optimal does not lead to a global optimum.  

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/fig_castel_dynamic_programming_vertical_50.png">
  <b>Figure 3.</b> Reduce the width of the image by 50 pixels using the Dynamic Programming method
</p>

### Decrease the image height
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/fig_praga_dynamic_programming_horizontal_50.png">
  <b>Figure 4.</b> Reduce the height of the image by 50 pixels using the Dynamic Programming method
</p>

### Amplifying the content of an image
Image width and length reduction algorithms may be used to amplify image content. To keep the image content as much as possible, the image is scaled with the magnification factor set by the user, and then it is applied the functions that perform the reduction operations on height and width to bring the image to its original size, preserving the aspect ratio.

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/data/arcTriumf.jpg" width="455">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/arcTriumf_dynamic_programming_amplificaContinut_05.png" width="455">
  <b>Figure 5.</b> Reference image (left), amplyfied content with 5% of the reference image (right).
</p>

### Remove object from the image

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/cum_merge_alg_de_elimobj.png">
  <b>Figure 6.</b> Remove object from the image
<p>
  
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/data/lac.jpg" width="497">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/lac_dynamic_programming_deleteObject.png" width="445">
  <b>Figure 7.</b> Original image(left). Results of the removing an object from the image (right).
<p>
<br/>

## Conclusions
The algorithm presented above has good results on a wide range of images compared to the usual resizing techniques. However, there are some limitations.  
One of these limitations is the content of an image. If the image is very condensed, in the sense that there are only portions with strong gradients, then the algorithm will have to eliminate areas with important content.  
Another limitation is the appearance of the image content. Some images, although not condensed, have the content arranged in a way that prevents the choice of paths that neglect important regions.  For example, we have an area with "interesting content" and a large gradient magnitude, which is surrounded by a much larger area with a small gradient magnitude. In this case, the portion with "interesting content" contributes little to the cost of paths passing through that area and therefore one of these paths may be a minimum cost path that is eliminated by the algorithm. It can be observed in Figure 4 that seams passing through the towers of constructions were removed.
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/SeamCarving/results/fig_colosseum.png">
  <b>Figure 8.</b> he original image, the resized image using the function <i>resize</i> in OpenCV and the image reduced by 200 pixels in width using the dynamic programming method
</p>
