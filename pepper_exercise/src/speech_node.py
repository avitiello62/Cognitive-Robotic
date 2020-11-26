#!/usr/bin/env python
import os
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from detector import Detector
from classmap import category_map as classmap
from pepper_exercise.srv import Say
from std_msgs.msg import String

#initialize node
rospy.init_node('speech_node')

#dictionary to track objects detected related to pepper position
pos_obj = {"left":{},"center":{},"right":{}}

#variable to track pepper head position
current_pos = None

#define callback to build string for pepper speech at the end of head movement
def rcv_head_position(msg):
    global current_pos
    global pos_obj
    current_pos=msg.data
    if current_pos=="end":
        content="I can see "
        positions = pos_obj.keys()
        for position in positions:
            content+=" at "+position+' : '
            classes = pos_obj[position].keys()
            if len(classes)<=0:
                content+="nothing, "
            for _cls in classes:
                content+=_cls+", "
        

        rospy.loginfo("START: Service call!!")
        rospy.loginfo(content)
        call_srv(content)

#call server_node service
def call_srv(text):
    rospy.wait_for_service('animated_say')
    animated_say = rospy.ServiceProxy('animated_say', Say)
    try:
        resp1 = animated_say(text)
    except rospy.ServiceException as exc:
        print("Service did not process request: " + str(exc)) 

#define callback to receive object detection results and store in the dictionary
def rcv_detection(msg):
    global current_pos
    detected_objs={}
    for d in msg.detections:
        c = d.results[0].id
        detected_objs[classmap[c]]=1
    pos_obj[current_pos]=detected_objs

#waiting for detector_node and head_node
sd = rospy.Subscriber("detection", Detection2DArray, rcv_detection)
sh = rospy.Subscriber("head_position", String, rcv_head_position)

try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")