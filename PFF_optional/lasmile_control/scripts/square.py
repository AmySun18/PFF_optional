#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from math import radians
PI = 3.1415926535897

class DrawASquare():
    def __init__(self):
        # initiliaze
        rospy.init_node('drawasquare', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10)

        self.length = input("Type your square length (meter): ")
        rospy.loginfo(self.length)
     
	# 5 HZ
        r = rospy.Rate(5);

	# create two different Twist() variables.  One for moving forward.  One for turning 45 degrees.

        # let's go forward at 1 m/s
        move_cmd = Twist()
        move_cmd.linear.x = 1
	# by default angular.z is 0 so setting this isn't required

        #let's turn 
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = 1; 
        

        while not rospy.is_shutdown():
	    
	    rospy.loginfo("Going Straight")
            current_distance = 0
            t0 = rospy.Time.now().to_sec()
            while(current_distance <self.length):
                self.cmd_vel.publish(move_cmd)
                t1 = rospy.Time.now().to_sec()
                current_distance = t1-t0 # go forward at 1m/s
                #rospy.loginfo(current_distance)
                r.sleep()
	    # turn 90 degrees
            current_angle = 0
	    rospy.loginfo("Turning")
            t0 = rospy.Time.now().to_sec()
	    while(current_angle<17.5): # 17 corresponding PI/2, wired...
                self.cmd_vel.publish(turn_cmd)
                t1 = rospy.Time.now().to_sec()
                current_angle = t1-t0 # turning
                r.sleep()
                
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        DrawASquare()
    except:
        rospy.loginfo("node terminated.")
