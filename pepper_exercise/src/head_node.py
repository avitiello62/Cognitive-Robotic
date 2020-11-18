#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from std_msgs.msg import String

rospy.init_node('test')
p = rospy.Publisher('/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=0)
p2 = rospy.Publisher('/head_position', String, queue_size=0)
s = JointAnglesWithSpeed()
s.joint_names=['HeadPitch', 'HeadYaw']
s.relative=0
s.speed=0.2
rate = rospy.Rate(0.2)
yaw_positions = [1,0,-1]
head_positions = ["left","center","right"]
while not rospy.is_shutdown():
    for i,pos in enumerate(yaw_positions):
        s.joint_angles=[0.2, pos]
        rospy.loginfo(s.joint_angles)
        p.publish(s)
        p2.publish(head_positions[i])
        rate.sleep()
    p2.publish("end")
    rate.sleep()
    #Pausa per un pò...