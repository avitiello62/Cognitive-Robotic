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
    current_pos=msg.data

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
    text="I can see"

    for d in msg.detections:
        c = d.results[0].id
        detected_objs[classmap[c]]=1

    if not current_pos=="end":
        pos_obj[current_pos]=detected_objs
        
    else:
        content=""
        positions = pos_obj.keys()
        for position in positions:
            rospy.loginfo("Ciao")
            content+=" at "+position
            classes = pos_obj[position].keys()
            for _cls in classes:
                content+=_cls+", "
        text+=content

        rospy.loginfo("START: Service call!!")
        call_srv(text)
 
    """
    if len(detected_objs)>0:
        for obj in detected_objs:
            text+=" "+obj
        text+=" "
        call_srv(text)
    else:
        text+=" Nothing "
        call_srv(text)
    """
    rospy.loginfo("TEXT: %s" % text)

sd = rospy.Subscriber("detection", Detection2DArray, rcv_detection)
sh = rospy.Subscriber("head_position", String, rcv_head_position)

try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")