# **Capstone project: Programming a Real Self-Driving Car**

This document presents the work developed for the capstone project of the SDC Nanodegree.
____________________________________________

Table of Contents:
1. Project Introduction
2. Build and usage Instructions

## 1. Project Introduction
This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. 

For this project, to objective is to write ROS nodes to implement core functionality of the autonomous vehicle system, including traffic light detection, control, and waypoint following! The code is tested first on a simulator.

The following is a system architecture diagram showing the ROS nodes and topics used in the project. It consists of 3 main modules: perception, planning,and control.

<img src="imgs/architecture.png" width="600">

### 1.1 Approach taken to complete the project

The project was completed by following the walkthrougs given in the course lessons. the order of execution was the following:

1. Complete a partial waypoint updater which subscribes to `/base_waypoints` and `/current_pose` and publishes to `/final_waypoints`.
2. Once the waypoint updater is publishing `/final_waypoints`, the waypoint_follower node will start publishing messages to the `/twist_cmd topic`. At this point, the controll part of the system can be completed. This includes modifying the `dbw_node.py` and `twist_controller.py` scripts.
After completing this step, the car drives in the simulator following the waypoints, ignoring the traffic lights.

3. Perform traffic light detection, and determining the closest waypoint to a red traffic light. For the detection of traffic lights, a YOLO V3 model was used. This model was previously trained on the COCO dataset, which contains 80 different classes (one of them is traffic light). This model is used to find traffic lights on the image, and then a simple algorithm is applied to find the light with the highest intensity. This algorithm determines whether a traffic light is on red or not.
4. Finally, the waypoint updater script is modified, so it can take into account the case when the car sees a red traffic light, and must stop.

## 2. Build and usage instructions
Please use **one** of the two installation options, either native **or** docker installation.

### 2.1 Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### 2.2 Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### 2.3 Usage

1. Clone the project repository
```bash
git clone https://github.com/baldesco/SDC_Capstone.git
```

2. Install python dependencies
```bash
cd SDC_Capstone
pip install -r requirements.txt
```
**Note:** This project needs opencv >= 3.4.3 in order to be able to perform object detection. If this is not possible, this part must be commented out. (The code is currently commented out in the parts that involve opencv>=3.4.3, and the light detection is just gotten from the simulator).

3. Download the files for the object detection model

The following command will create a new folder `yolo_model`, and download to it the weights and config files for the YOLO model, used for the detection of traffic lights. 
```bash
source download_model_files.sh
```
4. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
5. Run the simulator

### 2.4 Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

### 2.5 Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |

We are working on a fix to line up the OpenCV versions between the two.

