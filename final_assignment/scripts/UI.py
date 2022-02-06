#!/usr/bin/python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID 
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
import time
import math
'''
UI function:
this function will constantly ask the user to choose the current driving modality for the movements of the robot.
The following numbers rappresent the input the user has to insert in the UI to access a certain driving modality:

0: The robot will enter an IDLE STATE. In this modality no user input will be acceptet by the robot. The robot will not move until the modality will change.

1: This modality will activate an action that will drive automaticlly the robot toward a desired position. If the robot will not find the way to that certain coordinate position within 30 seconds from the beginning if the task, the driving will stop.

2: This driving option implements a simple teleop_key type of interface that will let the user drive the robot through the pressing of certain keyboard keys.  

3: The last modality implements a similar interface to the previous one but it also adds an obstacle avoidence capability. this added feature will prevent the user to drive the robot into a wall.
''' 

def action_client_init():

	global client 
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	
def action_client_cancel_goal():

	print("\033[1;31;40m GOAL CANCELED \033[0;37;40m \n")
	client.cancel_goal()
	
def main():
	
	#action_client_init()
	flag = 0
	while not rospy.is_shutdown(): 
		command = int(input('\033[0;37;40m Choose modality: \n'))
			
		# IDLE MODALITY
		if command == 0:
			if flag == 1:
				print("Canceling goal")
				#action_client_cancel_goal()
				flag=0
				
			rospy.set_param('active', 0)
			print("\033[1;35;40m Idle \033[1;31;40m")
			active_=rospy.get_param("/active")
			print(active_)
				
		# AUTONOMOUS DRIVE
		elif command == 1:
			if flag == 1:
				print("Canceling goal")
				#action_client_cancel_goal()
				flag=0
				
			rospy.set_param('active', 0)
			print("\033[1;32;40m Modality 1 is active, press '0' to cancel the target.")
			active_=rospy.get_param("/active")
			print("\033[0;37;40m Where do you want the robot to go?")
			des_x_input = float(input("\033[1;37;40m Insert x coordinate: "))
			des_y_input = float(input("\033[1;37;40m Insert y coordinate: "))
			rospy.set_param('des_pos_x', des_x_input)
			rospy.set_param('des_pos_y', des_y_input)
			rospy.set_param('active', 1)
			print("\033[1;32;40m Modality 1 is active.")
				
			action_client_init()
			flag = 1
			
		# KEYBOARD INTERFACE
		elif command == 2:
			if flag == 1:
				print("Canceling goal")
				flag=0
						
			rospy.set_param('active', 2)
			print("\033[1;33;40m Modality 2 is active.")
			active_=rospy.get_param("/active")
				
		# KEYBOARD INTERFACE + AVOIDENCE
		elif command == 3:
			if flag == 1:
				print("Canceling goal")
				flag=0
				
			rospy.set_param('active', 3)
			print("\033[1;34;40m Modality 3 is active.")
			active_=rospy.get_param("/active")
				
		# Message that will be sent whenever the keyboard input is different form the previously mentioned ones.
		else:
			print("\033[1;31;40m Wrong key, try again.")


if __name__ == '__main__':
	main()

