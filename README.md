# Cognitive-Robotic
In order to run the project you should follow these steps:

Run the following command to bring up Pepper:

```sh
roslaunch pepper_bringup pepper_full_py.launch nao_ip:=10.0.1.230
```
The following command starts detector node:
```sh
rosrun pepper_exercise detector_node 
```
When detector starts it register detection and detector_started topics and subscribes to image_head.

Run the following to start server_node:
```sh
rosrun pepper_exercise server_node.py 
```
The previous command launches a node which is a proxy for ALAnimatedSpeech service provided by naoQi API.
It provides itself a service to other nodes.

Run this to start speech_node:
```sh
rosrun pepper_exercise speech_node.py 
```
speech_node subscribes to detection and head_position. 
It takes detection results and semantic position to map detected objects to the right positions and
to allow pepper to say what it sees in each one.

Run the last command to start the head_node:
```sh
rosrun pepper_exercise head_node.py image:=/pepper_robot/camera/front/camera/image_raw
```
This is the final and a kind of synchronization node. When detector starts, it is notified and starts its work:
publish to /pepper_robot/pose/joint_angles to move the head and to /head_position for tracking semantic meaning of positions.
It waits for an image from pepper frontal camera and publish it to /image_head.
