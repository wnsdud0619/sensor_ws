#!/bin/bash
CAMERA=true
TOP_LIDAR=true
GPS=true

read -p "
use default setting?
-----------------------
enable camera = $CAMERA
enable lidar = $TOP_LIDAR
enable gps = $GPS
-----------------------
(y/n) " is_default

if [ $is_default = "y" ]
then
  sudo chmod 777 /dev/ttyUSB0 && source ./devel/setup.bash && roslaunch sensor_launch sensor.launch \
  enable_camera:=$CAMERA \
  enable_lidar:=$TOP_LIDAR \
  enable_gps:=$GPS
else
  read -p "is camera enable? (true, false): " CAMERA
  read -p "is lidar enable? (true, false): " TOP_LIDAR
  read -p "is gps enable? (true, false): " GPS  

  read -p "
use default setting?
-----------------------
enable camera = $CAMERA
enable lidar = $TOP_LIDAR
enable gps = $GPS
-----------------------
(y/n) " is_default
  if [ $is_default = "y" ]
  then
    sudo chmod 777 /dev/ttyUSB0 && source ./devel/setup.bash && roslaunch sensor_launch sensor.launch \
    enable_camera:=$CAMERA \
    enable_lidar:=$TOP_LIDAR \
    enable_gps:=$GPS
  fi
fi
