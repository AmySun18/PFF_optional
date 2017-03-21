#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import radians

class RobotMotion():
    def __init__(self):
         # initiliaze
        rospy.init_node('drawasquare', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)
     
	# 5 HZ
        r = rospy.Rate(5);
