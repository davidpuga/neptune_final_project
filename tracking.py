#! /usr/bin/env python

from collections import deque # deque is a package that creates list-like structures with versatile append functions
import numpy as numpy
import argparse
import imutils # not sure if I installed it correctly
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

