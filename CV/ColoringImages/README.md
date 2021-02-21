# Image Colorization using Convolutional Autoencoders

The project is an implementation of an image (or video) coloring algorithm (grayscale images) using a convolutional autoencoder(using Tensorflow 2.0).

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/ColoringImages/data/output_images/coast/coast128reusit3.png">
  <br/>
  <p align="center"><b>Figure 1. </b> Lab representaion (left), colored imaged (middle), original image (right).</p>
</p>

**Introduction.** Coloring images consists of transforming a grayscale image into an RBG image (BGR or Lab). The algorithm described below is based on the construction of an autoencoder that receives as input data the L channel, similar to a grayscale image and which predicts the ab channels of the Lab representation, sufficient to visualize the image in color. This type of autoencoder is called a *cross-channel autoencoder*.  
<br/>

<p align="center">
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/ColoringImages/data/output_images/forest/forest128reusit1.png">
  <br/>
  <p align="center"><b>Figure 2. </b> Lab representaion (left), colored imaged (middle), original image (right).</p>
</p>

The trained autoencoder consists only of convolutional layers and upsampling layers.
The architecture of the autoencoder:
* conv - 64 filters(the number of filters applied to the image) of 3x3, *activation function*=relu , *stride*=2 and *padding*=same (padding set with the *same* value completes the input with columns or rows of 0 until the result of applying the filter will be equal to the input size divided by stride)
* conv - 128 filters of 3x3, *activation function*=relu , *stride*=2 (the application stride of the filter on the two dimensions) and *padding*=same
* conv - 256 filters of 3x3, *activation function*=relu , *stride*=2 and *padding*=same
* conv - 512 filters of 3x3, *activation function*=relu , *stride*=1 and *padding*=same
* conv - 256 filters of 3x3, *activation function*=relu , *stride*=1 and *padding*=same
* upsampling layer with size=(2,2)
* conv - 128 filters of 3x3, *activation function*=relu , *stride*=1 and *padding*=same
* upsampling layer with size=(2,2)
* conv - 64 filters of 3x3, *activation function*=relu, *stride*=1 and *padding*=same
* upsampling layer with size=(2,2)
* conv - 2 filters of 3x3, *activation function*=tanh,*stride*=1 and *padding*=same
<br/>

#### Coloring video results
  <p> Original video on the left. Colored and resized video on the right. </p>
  
  [![Demo Coloring Video](https://j.gifs.com/D1zomq.gif)](https://github.com/danadascalescu00/FMI/blob/master/CV/ColoringImages/input_video.mp4)
  <img src="https://github.com/danadascalescu00/FMI/blob/master/CV/ColoringImages/input_video_colored.gif" width="150">
