#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from std_msgs.msg import String
from sensor_msgs.msg import Image


#variable to store the current image of frontal camera
current_img_msg = None

#initialize node and register Publisher topic to master node 
rospy.init_node('test')
p = rospy.Publisher('/pepper_robot/pose/joint_angles', JointAnglesWithSpeed, queue_size=0)
p2 = rospy.Publisher('/head_position', String, queue_size=0)
pi = rospy.Publisher("/image_head", Image, queue_size=0)
rate = rospy.Rate(0.1)

#set variable for head rotation
s = JointAnglesWithSpeed()
s.joint_names=['HeadPitch', 'HeadYaw']
s.relative=0
s.speed=0.2
yaw_positions = [1,0,-1]
head_positions = ["left","center","right"]
rate.sleep()

#define callback for image received from frontal_camera
def rcv_img(msg):
    global current_img_msg
    current_img_msg = msg

#start to rotate pepper's head when the detector is ready
def detector_started(msg): 
    for i,pos in enumerate(yaw_positions):

        #publish position to pepper's joint and track it on other topic
        s.joint_angles=[0.2, pos]
        rospy.loginfo(s.joint_angles)
        p.publish(s)
        p2.publish(head_positions[i])
        rate.sleep()

        #ask for an image from frontal camera being in left, center and right position
        current_img_msg =rospy.wait_for_message("image", Image)
        pi.publish(current_img_msg)
        rate.sleep()

        #set pepper to home position and notify other nodes that job's completed 
        if head_positions[i] == "right":
            p2.publish("end")        
            rate.sleep()
            s.joint_angles=[0.2, 0]
            rospy.loginfo(s.joint_angles)
            p.publish(s)
    rate.sleep()
  
#waiting for detector initialization
sd = rospy.Subscriber("detector_started", String, detector_started)
rospy.spin()


