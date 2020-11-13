#!/usr/bin/env python3
import os
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from detector import Detector
import ros_numpy # pip3 install git+https://github.com/eric-wieser/ros_numpy
#from naoqi_driver.naoqi_node import NaoqiNode
from classmap import category_map as classmap
from pepper_exercise.srv import Say




rospy.init_node('speech_node')
#pub = AnimatedSay()

def rcv_head_position(msg):
    pass

def call_srv(text):
    rospy.wait_for_service('animated_say')
    animated_say = rospy.ServiceProxy('animated_say', Say)
    try:
        resp1 = animated_say(text)
    except rospy.ServiceException as exc:
        print("Service did not process request: " + str(exc)) 

def rcv_detection(msg):
    #global pub
    detected_objs=[]
    text="message: 'I see"
    for d in msg.detections:
        c = d.results[0].id
        detected_objs.append(classmap[c])

    rospy.loginfo("START: Service call!!")

    if len(detected_objs)>0:
        for obj in detected_objs:
            text+=" "+obj
        text+=" ' "
        call_srv(text)
    else:
        text+=" Nothing' "
        call_srv(text)

    rospy.loginfo("TEXT: %s" % text)

sd = rospy.Subscriber("detection", Detection2DArray, rcv_detection)

try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")