# Neptune Computational Biology - Final Project


# Tracking post its

## Introduction and Goals

The goal of my project is to automatically identify the post-its on my webcam and track them.

The methods I will use to do this are:
* The [program](https://github.com/davidpuga/neptune_final_project/blob/master/tracking.py) I'm using is based on [this](http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/) and [this](http://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/) program.
* I will use the following python packages: deque, numpy, argparse, imutils, cv2, SciPy
* The scripts [range-detector](https://github.com/jrosebr1/imutils/blob/master/bin/range-detector) to obtain the HSV ranges for the orange post-it.


## Methods

The tools I used were... See analysis files at (links to analysis files).

## Results

![Figure 1](./Figure1.png?raw=true)

In Figure 1...

## Discussion

Identifying an object on a video can be done according to different variables of the object, such as color, shape or movement. In this program, I used the color of the post-its to differentiate them from the background and identify them.
In order to track an object, the object needs to be recognized as an entity throughout the video, i.e. from one frame to the next. My first script, which recognized and tracked a single post-it, identified the largest orange post-it and followed it. This truly tracks the post-it if only a single post-it is in the webcam's field of view, or if it is always the largest. But if more than one post-it is present and their relative sizes keep changing (because they get closer or further away from the webcam), the tracking will follow the largest post-it at any given frame, even if it is not the same one.
A solution to this, which also opens the possibility to track several post-its simultaneously, is to track 

The biggest difficulty in implementing these analyses was...

My

## References


