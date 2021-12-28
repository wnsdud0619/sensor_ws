cmake_minimum_required(VERSION 3.0.2)
project(tl_roi_img_pub)

find_package(catkin REQUIRED COMPONENTS
   autoware_perception_msgs
   sensor_msgs
)

catkin_package(CATKIN_DEPENDS
    autoware_perception_msgs
    sensor_msgs
)

catkin_package()