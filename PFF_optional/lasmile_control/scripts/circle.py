#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math
PI = 3.1415926535897

class DrawACircle():
    def __init__(self):
        # initiliaze
        rospy.init_node('drawacircle', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.radius = input("Type your circle radius (meter): ")
        rospy.loginfo(self.radius)
     
	# 5 HZ
        r = rospy.Rate(10);


        # In a circle, 
        move_cmd = Twist()
        move_cmd.linear.x  = float(self.radius*0.1)
        move_cmd.angular.z = float(self.radius*0.1) # real vel PI=18sec

        while not rospy.is_shutdown():	
            rospy.loginfo("Run along a circle")   
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)
                
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        DrawACircle()
    except:
        rospy.loginfo("node terminated.")
