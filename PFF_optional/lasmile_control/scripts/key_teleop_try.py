#!/usr/bin/env python
import rospy
import numpy as np
from math import radians
from geometry_msgs.msg import Twist
PI = 3.1415926535897


def robotmotion():
    #Starts a new node
    rospy.init_node('robot', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    turn_msg= Twist()

    # 5Hz
    r=rospy.Rate(5)

    # Receiveing the user's input
    print("Let's control your robot")
    mode = input("Select a control mode: 1: key_board, 2: circle, 3: square ")
    if mode==1:
        msg = """
    
       Moving direction:
            W   
       A   Robot   D
            X   
       anything else : stop
       --------------------------------------------------
       """
        print(msg)
    elif mode==2:
        print("The robot will run along a circle")
        radius = input("Type your circle radius (meter): ")
        vel_msg.angular.z=1/(2*PI);
        vel_msg.linear.x=radius/(2*PI);
        vel_msg.linear.y=0
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        while not rospy.is_shutdown():
            velocity_publisher.publish(vel_msg)
            r.sleep()
    
        velocity_publisher.publish(Twist())
    else:
        print("The robot will run along a square")
        length = input("Type your square length (meter):") 
        #robotspeed=np.array([[1,0],[0,1],[-1,0],[0,-1]])      
        vel_msg.linear.z=0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
	vel_msg.angular.z = 0
 	num=0
        while not rospy.is_shutdown():          
	    vel_msg.linear.x=0.1
	    vel_msg.angular.z=0
            for x in range(0, int(50*length)):
	        velocity_publisher.publish(vel_msg) 
    		r.sleep();
            current_angular=0
	    turn_msg.linear.x=0
	    turn_msg.angular.z=radians(45);
	    turn_msg.linear.y=0
            turn_msg.linear.z=0
            turn_msg.angular.x = 0
            turn_msg.angular.y = 0
	    for x in range(0,10):
                velocity_publisher.publish(turn_msg) 

    #Stop the robot
    #rospy.signal_shutdown('Shutdown')

if __name__ == '__main__':
    try:
        # Testing our function
        robotmotion()
    except rospy.ROSInterruptException:
        pass
