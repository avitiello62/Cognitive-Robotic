#!/usr/bin/env python3
import os
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from detector import Detector
import ros_numpy # pip3 install git+https://github.com/eric-wieser/ros_numpy
#from naoqi_driver.naoqi_node import NaoqiNode
from classmap import category_map as classmap



'''
class AnimatedSay(NaoqiNode):
    def __init__(self):
        NaoqiNode.__init__(self,'animated_speech')
        self.connectNaoQi()
        pass
    def say(self,message):
        rospy.loginfo("START: %s" % data.message)
        self.speech.say(message)
        rospy.loginfo("END: %s" % data.message)
        
    def connectNaoQi(self):
        self.speech=self.get_proxy("ALAnimatedSpeech")
        
'''
rospy.init_node('speech_node')
#pub = AnimatedSay()


def rcv_detection(msg):
    #global pub
    detected_objs=[]
    text='I see '
    for d in msg.detections:
        c = d.results[0].id
        detected_objs.append(classmap[c])
    for obj in detected_objs:
        text+=obj
        text+=' '
    rospy.loginfo("START: %s" % text)
    #pub.say(text)




sd = rospy.Subscriber("detection", Detection2DArray, rcv_detection)

try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")