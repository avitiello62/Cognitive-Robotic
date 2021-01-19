#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from std_msgs.msg import String
from pepper_exercise.msg import DetectionInfo
from utils.HeadHandler import HeadHandler
from utils.DetectionInfoHandler import DetectionInfoHandler

class PepperHandler:

    def __init__(self):
        self._head_handler = HeadHandler()
        self._custom_detection_info=DetectionInfoHandler()
        self.head_position={'left':1,'center':0,'right':-1,'home':0}

    def turn(self,pos):        
        self._head_handler.set_joint_angles([0.2, self.head_position[pos]])
        self._head_handler.publish_joint()
        rospy.loginfo("i'm going to "+pos+ ' position')
    
    def publish_detection(self,detections,head_position):
        self._custom_detection_info.publish_detection_message(detections,head_position)

    
    
    