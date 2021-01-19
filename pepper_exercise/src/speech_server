#!/usr/bin/python
import rospy
from naoqi_driver.naoqi_node import NaoqiNode
from pepper_exercise.srv import Say

class AnimatedSay(NaoqiNode):
    def __init__(self):
        NaoqiNode.__init__(self,'animated_speech')
        #set pepper ip
        self.pip="10.0.1.230"
        self.connectNaoQi()    
        pass

    def say(self,data):
        rospy.loginfo("SPEECH SERVICE CALL: %s" % data.message)
        self.speech.say(data.message)
        #rospy.loginfo("END: %s" % data.message)
        return True
        
    def connectNaoQi(self):
        self.speech=self.get_proxy("ALAnimatedSpeech")
        self.s = rospy.Service('animated_say', Say, self.say)

if __name__=="__main__":
    pub = AnimatedSay()
    rospy.spin()