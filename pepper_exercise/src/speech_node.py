#!/usr/bin/env python
import os
import rospy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose

from classmap import category_map as classmap
from pepper_exercise.srv import Say
from std_msgs.msg import String
from pepper_exercise.msg import DetectionInfo

# initialize node
rospy.init_node('speech_node')

# dictionary to track objects detected related to pepper position
pos_obj = {"left": {}, "center": {}, "right": {}}


# call server_node service
def call_srv(text):
    rospy.wait_for_service('animated_say')
    animated_say = rospy.ServiceProxy('animated_say', Say)
    try:
        resp1 = animated_say(text)
    except rospy.ServiceException as exc:
        print("Service did not process request: " + str(exc))


def rcv_detection_and_head_pos(msg):

    global pos_obj
    current_pos = msg.head_position
    if current_pos != 'home':
        detected_objs = {}
        for d in msg.detections:
            c = d.results[0].id
            detected_objs[classmap[c]] = 1
        pos_obj[current_pos] = detected_objs
    else:
        content = "I can see "
        for position in ['left', 'center', 'right']:
            content += " at "+position+' : '
            classes = pos_obj[position].keys()
            if len(classes) <= 0:
                content += "nothing, "
            for _cls in classes:
                content += _cls+", "
    
        call_srv(content)
        


shd = rospy.Subscriber("detection_and_head_position",
                       DetectionInfo, rcv_detection_and_head_pos)
try:
    rospy.spin()

except KeyboardInterrupt:
    print("Shutting down")
