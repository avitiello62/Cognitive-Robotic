#!/usr/bin/env python
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed
from std_msgs.msg import String
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray
from pepper_exercise.srv import Detect
from HeadHandler import HeadHandler
from pepper_exercise.msg import DetectionInfo
from PepperHandler import PepperHandler


#initialize node and register Publisher topic to master node 
rospy.init_node('synchronization_node')
pub_detection = rospy.Publisher('detection_and_head_position', DetectionInfo, queue_size=0)
rate = rospy.Rate(0.2)
pepper_handler=PepperHandler()


#define function to call service
def detect_image_client(img):
    rospy.wait_for_service('detect_service')
    rospy.loginfo("Detection service invoked")
    try:
        detect_service = rospy.ServiceProxy('detect_service', Detect)
        msg = detect_service(img)
        return msg.det
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


def apply_detection():
    current_img_msg = rospy.wait_for_message("/pepper_robot/camera/front/camera/image_raw", Image)
    detection_msg=detect_image_client(current_img_msg)
    return detection_msg

apply_detection()
rospy.loginfo("Detection service ready")

for pos in ['left','center','right']:
    
    pepper_handler.turn(pos)
    rospy.sleep(3.0)
    detection_msg=apply_detection() 
    pepper_handler.publish_detection(detection_msg.detections,pos)
    

pepper_handler.turn('home')
rospy.sleep(1.0)
pepper_handler.publish_detection([],'home')
  

