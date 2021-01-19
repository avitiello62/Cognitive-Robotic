#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from std_msgs.msg import String

class HeadHandler:
    def __init__(self):
        self._pub_joint = rospy.Publisher(
            '/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=0)
        self._s = JointAnglesWithSpeed()
        self.init_joint()
       
       
        
    def init_joint(self):
        self._s.joint_names = ['HeadPitch', 'HeadYaw']
        self._s.relative = 0
        self._s.speed = 0.2


    def set_joint_angles(self,angles):
        self._s.joint_angles = angles
        
    def publish_joint(self):
        self._pub_joint.publish(self._s)
        
    
    
    