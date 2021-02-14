

# Create mosaic images

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#implementation-of-algorithms-for-obtaining-mosaic-images">Implementation of algorithms for obtaining mosaic images</a></li>
  </ol>
</details>


## About the project
A mosaic image (called a mosaic) is obtained by replacing pixel blocks in a reference image with small images (we call them mosaic pieces) from a given collection. Replacing 
the pixel blocks with pieces is done so that the resulting mosaic approximates as well as possible the reference image.  

<p>
  <img src ="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/ferrari.jpeg" width="480">  
  <img src ="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_ferrari_caroiaj_100.png" width="480">
  <b>Figure 1.</b> Mosaic image: for the reference image on the left we get the mosaic on the right. The mosaic pieces are chosen from a collection of 500 images (mosaic pieces), where each image represents a flower.
</p>
<br/>

## Usage
To get the mosaic image, run the **_run_project.py_** script. This script sets the reference image for which the mosaic will be made and sets various parameters including:
  - the name of the director in which the collection of small images is located and which will constitute the pieces of the mosaic;
  - the format of the images in the collection ('jpg', 'jpeg', 'png', 'tiff', etc). All pieces of the mosaic must have the same format.
  - the number of horizontal pieces of the mosaic (set by default with the value 100), which defines the dimensions of the resulting mosaic;
  - ways of arrangement of the mosaic pieces. In this project there arre two ways of arrangement:
    1. arrangement on a grid, in which the pieces are placed one after the other and blend perfectly, without overlaps;
    2. at random, in which the parts are placed at random positions in the mosaic, with overlaps.
  - the criterion according to which the pieces are chosen for making the mosaic. Two criteria are used in this project:
    1. random
    2. according to the average color  
<br/>

## Implementation of algorithms for obtaining mosaic images
### 3.1 Loading mosaic pieces  
The _load_pieces_ function performs the operation of reading the mosaic pieces from the directory containing the collection of pieces. If the _show_small_images_ parameter is set, the first 100 pieces of mosaic will be displayed in a figure at the end.  
The user has the option to upload a GRAYSCALE image, in which case the grayscale parameter will be set and the mosaic pieces will be converted to GRAYSCALE format using the conversion:
<p align="center"><b> Y = 0.2125R + 0.7152G + 0.0721B </b></p>
<br/>

### 3.2 Calculating the dimensions of the mosaic  
We want to get an image that keeps the ratio between the width and height of the reference image. For this, the size of a mosaic image must be determined, considering the number of pieces horizontally, <i>num_pieces_horizontal</i> (can be set by the user). Based on this parameter, the aspect ratio of the reference image and the size of a mosaic piece, it will be determined the number of pieces on vertical, <i>num_pieces_vertical</i> . The width of the mosaic is equal to the product between the number of pieces horizontally and the width of the piece of the mosaic. The height of the mosaic is calculated to preserve the original aspect ratio of the reference image using the following formula:
<p align="center"> <img src="https://render.githubusercontent.com/render/math?math=H_{0} = \frac{W}{H} * (W * num\_pieces\_horizontal)"> </p>
where H, W represents the height, respectively the width of the initial image, and H<sub>0</sub> represents the new dimension of the mosaic image.  
The number of vertical pieces is given by the ratio between the new height of the reference image, H0, and the height of the mosaic piece. In the construction of the mosaic, we will use the resized reference image using the compute_dimensions function.  
<br/>

### 3.3 Adding mosaic pieces  
The pieces are added to obtain a mosaic as similar as possible to the resized reference image, taking into account the layouts (grid or random) or the shapes of the pieces (rectangular or hexagonal). The arrangement modes, as well as the shape of the mosaic pieces, represent the parameters that can be set by the user.  
The two criteria for mosaic pieces are:
  1. random - the pixel blocks in the resized reference image are replaced with randomly selected parts
  2. based on the Euclidian distance between the average colors - the pixel blocks in the resized reference image are replaced with mosaic pieces so that the average color of the selected mosaic piece is as close as possible to the average color of the current block
<br/>

### 3.4 Obtaining the mosaics for the grid layout and Euclidean distance criterion of average colors
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_liberty_caroiaj_25.png" width="310" >  
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_liberty_caroiaj_50.png" width="310" >
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_liberty_caroiaj_75.png" width="310" >
  <b>Figure 2.</b> Mosaic images with 25, 50 and 75 pieces.
</p>

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_liberty_caroiaj_100.png">
  <b>Figure 3.</b> Mosaic imag with 100 pieces.
</p>

It can be seen in the images in Figure 2 and Figure 3 that as the number of parts of the mosaic increases, we obtain an image that better and better approximates the reference image.  
<br/>

### 3.5 Obtaining mosaics for the random arrangement and the criterion of the Euclidean distance between the average colors
At each iteration of the algorithm, a position is randomly selected to place the upper left corner of the resized image. To avoid the exact overlapping pieces (there may be overlapping partial pieces), the positions are chosen randomly from a "poll" of the candidates, a linear vector that holds the positions unelected. The algorithm ends when the entire grid is covered.
<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/tomJerry.jpeg" width="475">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_tomJerry_aleator_100.png" width="475">
  <b>Figure 4.</b> Reference image (left). Mosaic image with 100 pieces for the random arrangement and the criterion of the Euclidean distance between the average colors (right).
</p>
<br/>

### 3.6 Obtaining the mosaics for the grid arrangement mode, the criterion of the Euclidean distance between the average colors and the property that no two adjacent pieces are identical
<p align="center"> 
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/obama.jpeg" width="480">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_obama_caroiaj_vecini.png" width="480">
  <b>Figure 5.</b> Reference image (left). Mosaic image with 100 pieces for the grid arrangement mode, the criterion of Euclidian distance between average colors and the property that no two adjancent pieces are identical (right).
</p>
<br/>

### 3.7 Obtaining mosaics for the grid layout and the criterion of the Euclidean distance between the average colors in the hexagonal pieces  
<p align="center"> 
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/ferrari.jpeg" width="480">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_ferrari_hexagon_100.png" width="480">
  <b>Figure 6.</b> Reference image (left). Mosaic image with 100 hexagonal pieces for the grid arrangement mode, the criterion of Euclidian distance between average colors (right).
</p>
<br/>

### 3.8 Obtaining mosaics for the grid layout and the criterion of the Euclidian distance between the average colors in the hexagonal pieces with the property that there are not any adjancent pieces identical  
<p align="center"> 
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/tomJerry.jpeg" width="480">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_tomJerry_hexagonal_vecini_95.png" width="480">
  <b>Figure 7.</b> Reference image (left). Mosaic image with 95 hexagonal pieces for the grid arrangement mode, the criterion of Euclidian distance between average colors and the property that there are not any adjancent pieces identical (right).
</p>
<p align="center"> 
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/imaginiTest/romania.jpeg" width="480">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/MosaicGenerator/data/results/mosaic_romania_hexagonal_vecini_105.png" width="480">
  <b>Figure 8.</b> Reference image (left). Mosaic image with 105 hexagonal pieces for the grid arrangement mode, the criterion of Euclidian distance between average colors and the property that there are not any adjancent pieces identical (right).
</p>
<br/>
<br/>
