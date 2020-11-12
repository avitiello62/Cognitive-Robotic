#!/usr/bin/python
import rospy
from std_msgs.msg import Float32MultiArray



def publisher():


    pub=rospy.Publisher('ctrl', Float32MultiArray)

    rospy.init_node('my_node_controller')
    msg=Float32MultiArray()
    msg.data=[0,0]

    r = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        a=input("Inserisci primo angolo:")
        b=input("Inserisci secondo angolo:")
        msg.data=[float(a*(3.1415)/180),float(b*(3.1415/180))]
        pub.publish(msg)
        r.sleep()

    

if __name__ == '__main__':
    publisher()