#!/bin/sh

docker run -it -v ${PWD}/:/ws --name gazebo gazebo

#For windows: docker run -it -v %cd%/:/ws --name gazebo gazebo
