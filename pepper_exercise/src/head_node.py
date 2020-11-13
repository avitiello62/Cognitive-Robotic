#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed

rospy.init_node('test')
p = rospy.Publisher('/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=0)
s = JointAnglesWithSpeed()
s.joint_names=['HeadPitch', 'HeadYaw']
s.relative=0
s.speed=0.2
rate = rospy.Rate(0.2)
a = True
while not rospy.is_shutdown():
    a = not a
    s.joint_angles=[0.2, 1.0 if a else -1.0]
    rospy.loginfo(s.joint_angles)
    p.publish(s)
    rate.sleep()