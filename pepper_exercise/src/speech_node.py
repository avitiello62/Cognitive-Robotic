#!/usr/bin/env python
import os
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from detector import Detector
#from naoqi_driver.naoqi_node import NaoqiNode
from classmap import category_map as classmap
from pepper_exercise.srv import Say
from std_msgs.msg import String



rospy.init_node('speech_node')
#pub = AnimatedSay()
pos_obj = {"left":{},"center":{},"right":{}}
current_pos = None


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

def call_srv(text):
    rospy.wait_for_service('animated_say')
    animated_say = rospy.ServiceProxy('animated_say', Say)
    try:
        resp1 = animated_say(text)
    except rospy.ServiceException as exc:
        print("Service did not process request: " + str(exc)) 

def rcv_detection(msg):
    global current_pos
    detected_objs={}
    for d in msg.detections:
        c = d.results[0].id
        detected_objs[classmap[c]]=1

    
    pos_obj[current_pos]=detected_objs
    

    

sd = rospy.Subscriber("detection", Detection2DArray, rcv_detection)
sh = rospy.Subscriber("head_position", String, rcv_head_position)

try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")