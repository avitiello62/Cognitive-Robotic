from pepper_exercise.msg import DetectionInfo
import rospy

class DetectionInfoHandler:
    def __init__(self):
        self._message=DetectionInfo()
        self._pub_detection = rospy.Publisher('detection_and_head_position', DetectionInfo, queue_size=0)

    def publish_detection_message(self,detections,head_position):
        self._message.detections=detections
        self._message.head_position=head_position
        self._pub_detection.publish(self._message)
        rospy.loginfo("Detection and head pos published")

