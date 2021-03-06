#! /usr/bin/env python
import rospy, math
import numpy as np
import sys, termios, tty, select, os
from geometry_msgs.msg import Twist
 
class KeyTeleop(object):
  cmd_bindings = { 'w':np.array([1,0]),                
                  'a':np.array([0,1]),
                  'd':np.array([0,-1]),
                  'x':np.array([-1,0])                 
                  }
  def init(self):
    # Save terminal settings
    self.settings = termios.tcgetattr(sys.stdin)
    # Initial values
    self.inc_ratio = 0.1
    self.speed = np.array([1.0, 1.0])
    self.command = np.array([0, 0])
    self.update_rate = 10   # Hz
    self.alive = True
    # Setup publisher
    self.pub_twist = rospy.Publisher('/cmd_vel', Twist)
 
  def fini(self):
    # Restore terminal settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
 
  def run(self):
    try:
      self.init()
      self.print_usage()
      r = rospy.Rate(self.update_rate) # Hz
      # Receiveing the user's input
      mode = self.get_key()
      if mode=="k": 
          ch = self.get_key()
          self.process_key(ch)
          self.update()
          r.sleep()
          while not rospy.is_shutdown():
              ch = self.get_key()
              self.process_key(ch)
              self.update()
              r.sleep()
      elif mode=="c":
          radius = input("Type your circle radius (meter): ")
      elif mode=="s":
           length = input("Type your square length (meter):")
      else:
          fini(self)
          
    except rospy.exceptions.ROSInterruptException:
      pass
    finally:
      self.fini()
 
  def print_usage(self):
    msg = """
    Keyboard Teleop that Publish to /cmd_vel (geometry_msgs/Twist)
    Copyright (C) 2013
    Released under BSD License
    Let's control your robot!
    --------------------------------------------------
    
    K:Key_board Control 
    Moving around:
            W   
      A   Robot   D
            X   
    C: circle mode
    S: square mode
    anything else : stop
 
    G :   Quit
    --------------------------------------------------
    """
    self.loginfo(msg)
    self.show_status()
 
  # Used to print items to screen, while terminal is in funky mode
  def loginfo(self, str):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
    print(str)
    tty.setraw(sys.stdin.fileno())
 
  # Used to print teleop status
  def show_status(self):
    msg = 'Status:\tlinear %.2f\tangular %.2f' % (self.speed[0],self.speed[1])
    self.loginfo(msg)
 
  # For everything that can't be a binding, use if/elif instead
  def process_key(self, ch):
    if ch == 'h':
      self.print_usage()
    elif ch in self.cmd_bindings.keys():
      self.command = self.cmd_bindings[ch]
    elif ch == 'c':
      print("The robot will run along a circle")
      #print("Type your circle radius (meter):")
      radius = input("Type your circle radius (meter):")     
      self.command = np.array([radius, 1])  
    elif ch == 'g':
      self.loginfo('Quitting')
      # Stop the robot
      twist = Twist()
      self.pub_twist.publish(twist)
      rospy.signal_shutdown('Shutdown')
    elseif:
      self.command = np.array([0, 0])
 
  def update(self):
    if rospy.is_shutdown():
      return
    twist = Twist()
    cmd  = self.speed*self.command
    twist.linear.x = cmd[0]
    twist.angular.z = cmd[1]
    self.pub_twist.publish(twist)
 
  # Get input from the terminal
  def get_key(self):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    return key.lower()
 
if __name__ == '__main__':
  rospy.init_node('keyboard_teleop')
  teleop = KeyTeleop()
  teleop.run()
