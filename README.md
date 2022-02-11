#  [Research_Track_1](https://unige.it/en/off.f/2021/ins/51201.html?codcla=10635) , [Robotics Engineering](https://courses.unige.it/10635) ([UNIGE](https://unige.it/it/)) : Final assignement
## Robot Operating System <img height="30" src="https://github.com/Fabioconti99/RT1_Assignment_2/blob/main/images/ros.png"> & Python <img height="30" src="https://github.com/Fabioconti99/RT1_Assignment_1/blob/main/images/python.png">
### Professor. [Carmine Recchiuto](https://github.com/CarmineD8)


--------------------
Project objectives
--------------------
This project is about the development of a software architecture of the control of a mobile robot.
The architecture should be able to get the user request, and let the robot execute one of the following behaviors (depending on the user's input):

* **Autonomously reach an x,y coordinate** inserted by the user,
* Let the user **drive** the robot **with the keyboard**,
* Let the user drive the robot assisting them to **avoid collisions**.

The user will be able to change the driving modality through a **UI interface**:
* pressing **[1]** the interface will ask the user to insert the *x* and *y* coordinates. The robot will eventually try to drive autonomously to those coordinates.
* pressing **[2]** the UI will activate a simple *teleop_key* interface that will let the user drive the robot with keyboard inputs.
* pressing **[3]** the UI will add to the previous modality an extra a driving assistency feature. The user will be assisted by a **collision avoidence** layer that will prevent the robot to hit the walls if it gets too close to them. 

The software will rely on the `move_base` and `gmapping` pakages for localizing the robot and plan the motion.

* The `move_base` package will provide an implementation of an *action* that, given a goal in the world, the robot will attempt to reach it with a mobile base. (Actions are services which are notexecuted automatically, and thus may also offer some additional tools such as the possibility of cancelling the request. 
* The `gmapping` pakage contains the algorithm based on a *particle filter* (approach to estimate a probability density) needed for implementing Simultaneous Localization and Mapping (SLAM). Needed by the `gmapping` package. 

The package will be tested on a simulation of a mobile robot driving inside of a given enviroment. The simulation and visualization are run by two following programs: 

* **Rviz**: which is a tool for ROS Visualization. It's a 3-dimensional visualization tool for ROS. It allows the user to view the simulated robot model, log sensor information from the robot's sensors, and replay the logged sensor information. By visualizing what the robot is seeing, thinking, and doing, the user can debug a robot application from sensor inputs to planned (or unplanned) actions.

* **Gazebo**: which is the 3D simulator for ROS. 

Picture of the **Gazebo Enviroment**:

![alt text](https://github.com/Fabioconti99/RT1_Assignment_2/blob/main/images/map.png) 

Picture of the **Robot inside the enviroment**:

![alt text](https://github.com/Fabioconti99/RT1_Assignment_2/blob/main/images/map.png) 

--------

Installing and running
----------------------
The simulation requires the following steps before running:

* A [ROS Noetic](http://wiki.ros.org/noetic/Installation) installation,

* The download of the `slam_gmapping` package form the *Noetic* branch of the [teacher's repository](https://github.com/CarmineD8/slam_gmapping.git )

Run the following command from the shell:
```bash
git clone https://github.com/CarmineD8/slam_gmapping.git
```

* The download of the **ROS navigation stack** (run the following command from the shell)

Run the following command from the shell:
```bash
sudo Apt-get install ros-<your_ros_distro>-navigation
```

* And the and the clone of the [Current repository](https://github.com/Fabioconti99/RT1_Assignment_3 ). After downloading the repository, you should take the `final_assignment` directory included in the repo and place it inside the local workspace directory.

Run the following command from the shell:
```bash
git clone https://github.com/Fabioconti99/RT1_Assignment_3
```

The *Python* scripts I developed define a **user inteface** that will let the user switch between driving modalities.
The **four scripts** provided are the following: 

* UI.py: Which rappresents a kind of menu where the user can switch between driveing modalites.

* go_to_desired_pos: This script implements an *Action* client-service comunication that will manage to drive the robot to a choosen position in the enviroment.

* my_teleop_twist_keyboard: Which will let the user directly drive the robot with keyboard inputs.

* teleop_avoid.py: Which will let the user directly drive the robot with keyboard inputs.

* avoidence.py: The last modality adds an obstacle avoidence capability to the second modality thanks to the custom message `Avoid.msg`. This added feature will prevent the user to drive the robot into a wall.

## Running the simulation

To Run the simulation easily I added two *launch files* to the package. 

* launch_nodes.launch: That will launch the previously mentioned nodes through the use of the *Xterm* terminal. It will also initialize some **parameters** that will be used by the nodes during execution.

* launch_All.launch: that will *include* all the launch files needed for running the whole simulation all at once.

Run the following command from the shell to activate all the nodes:
```bash
roslaunch final_assignment launchAll.launch
```

This kind of execution needs the Xterm terminal to be installed. If the it's not already installed you can download it with the following shell command:

```bash

sudo apt-get install -y xterm
```
------
NODES Description
-------------------

## UI node: UI.py

This node controls the robot's driving capabilities inside the enviroment. The **UI function** will command the robot to drive with a certain **Modality** inside the Gazebo map. Thanks to this node, the User will be able to interact with the simulation choosing the driving bod throgh certain keyboard inputs.

Driving modalities related to their keyboard inputs:

* The keyboard input **[0]** resets the current driving modality.
* The keyboard input **[1]** will start the autonomous drive towards a certain locatin in the map choosen by the user.
* The keyboard input **[2]** will start a simple teleop-key interface.
* The keyboard input **[3]** will add to the previus interface an avoidence layer.

Thanks to the `launch_nodes.launch` launch file, I added **three parameters** to the project for managing the *different activation state* of all the nodes involved in the project.
The three parametrs are:

* **Active**: This parameter manages the current state of the project's ROS node chain. Once the program is launched, the parameter is set to be in *idle state* (0 state). In the beginning one of the nodes will be in their active state. The UI node is capable of managing the change of value of this parameter thanks to the retrieved user input. A simple legend will tell the user what button to press for running a certain driving modality. The user input will change the value of the parameter and all the nodes will either keep their current idle state or switch to a running state. An If-Statement inside every node manages this modality switch.

* **Posion X and Position Y**: Also this two parameters are retrived by an input user managed in the UI node. Once the user will select the **first modality [1]** the UI interface will also ask for an X and Y coordinate. This data rappresents the position we want the robot to go to. If the user wants to stop the robot's motion he will only need to either input another driving modality or to set the project idle state.

The UI node will also keep the user updated on the current modality thanks to the on screen messages sent at every state switch. Some flags will keep track of the current modality based on the UI inputs.


------
## Autonomous drive mode: go_to_desired_pos.py

This node implements the autonomous driving capability. The script exploits an **action client** (*actionlib* library) istance to establish a direct comunication with the mobile robot and set and cancel location goals.

The Action Client-Service communicate via a "ROS Action Protocol", which is built on top of ROS messages. The client and server then provide a simple API for users to request goals (on the client side) or to execute goals (on the server side) via function calls and callbacks. 
Through out the coding of this node I implemented only the *Actionclient* side of the whole structure using the already existing server of the following action messages:

* `MoveBaseAction`
* ` MoveBaseGoal`

The following picture shows a graphical rappresentation of the ROS-Action protocol: 


* *goal*: used to send new goals to server
* *cancel*: used to send cancel requests to server
* *status*: used to notify clients on the current state of every goal in the system
* *feedback*: used to send clients periodic auxiliary information for a goal
* *result*:  used to send clients one-time auxiliary information about the completion of a goal

In order for the client and server to communicate, I should define a few messages on which they communicate. This defines the Goal, Feedback, and Result messages with which clients and servers communicate. In the code code I only used the Goal message beacause that was the one message needed for fullfilling the project aim. 

Thanks to the Actionlib feature the goal message can be sent to an ActionServer by an ActionClient. In the case of my project, the goal is to move the robot's base position, the goal would be a MveBaseGoal message that contains information about where the robot should move to in the world. For controlling all the robot position in space, the goal would contain the *target_pose* parameters (stamp, orientation, target position, etc).

 ### Main functions used
 
the following function sets the standard istances of the position I want to achive and it also initialize the client side of the action:

```python
def action_client_init():

    global client 
    global goal 
    
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction) # Initialization of the action client.
    client.wait_for_server()                            # Waiting for the server to get ready.
    
    goal = MoveBaseGoal()                         # Initialization of the goal message.
    goal.target_pose.header.frame_id = "map"            # Setting up some parameters of the goal message.
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.orientation.w = 1.0
    
# Call Back used for setting up a timeout to the robot's current task.
def my_callback_timeout(event):
    if active_==1:
        print ("\033[1;31;40m Goal time expired\033[0;37;40m :" + str(event.current_real)+st)
        print("The robot didn't reach the desired position target within a 1min time span\n")
        rospy.set_param('active', 0)
```

Once the node gets to its active state, the retrived info on the goal position will be retrived from the newly set parameters and inserted inside the goal message structure. This operation is taken care by the followiong "set-goal" function: 

```python
def action_client_set_goal():

    goal.target_pose.pose.position.x = desired_position_x
    goal.target_pose.pose.position.y = desired_position_y
    print("\033[1;33;40m START AUTONOMOUS DRIVE"+st+"\033[0;37;40m \n")
    client.send_goal(goal,done_cb)
```
The following image shows the Rviz graphical interface once the goal is set:



The argument `done_cb` of the `send_goal` function is a special call-back function needed for retriving info on the goal reaching *status*. This function retrives info directly from the server side. There are many different values associated to the status parameter during execution ending. The only one used in the code is the *status 3* related to the goal achivement:

```python
def done_cb(status,result):
    
    global flag_goal
    
    if status==3:
        print("\033[1;34;40m goal achived!"+st+"\033[0;37;40m \n")
        flag_goal = 1
```

Since the info retrived by this function is strictly determined by the server, I choose to not retrive any other status. There exist a status for retriving also a *timeout* ending for the robot. I decided to not use it because the actual time is set directly by the server.
The folliwing function sets a timer expiration goal that is localy set to 1 minute. Once it expires it will automatically cancel the goal.

```python
def my_callback_timeout(event):
    if active_==1:
        print ("\033[1;31;40m Goal time expired\033[0;37;40m :" + str(event.current_real)+st)
        print("The robot didn't reach the desired position target within a 1min time span\n")
        rospy.set_param('active', 0)
        
```

Thorough out the whole execution, thanks to the following callback, the program will print the actual position on screen with a 10hz rate. The actual position is not retrived by the *action feedback* but from a subscription to the odometry topic `/odom`. 

```python
def clbk_odom(msg): 
    global position_
    position_ = msg.pose.pose.position
    
```

Picture of the standard GUI window of the first modality:


The normal `cancel_goal` is activated once the robot gets back into its idle state. The cancel call is managed by all the flags that determine the current state of the process.

```python
# The active value is not set to 1
else:
    # Initial idle state 
    if flag == 0 and flag_2==0:
        
        print("\033[1;31;40m STOP MODALITY 1 \033[0;37;40m \n")
        flag = 1
    
    # Idle state the node will get to once the robot gets stopped by the user.
    if flag == 0 and flag_2==1:
        
        # Flag needed to know if the goal is reached or not
        if flag_goal==1:
            # If the goal is reached I will not cancel the goal because. 
            print("\033[1;31;40m STOP MODALITY 1 "+st+"\033[0;37;40m")
            flag = 1
            flag_2 = 0
            flag_goal = 0
    
        else:
            # If the goal is not reached once the user switches modality or the time expires with the time-out.
            print("\033[1;31;40m GOAL CANCELED, STOP MODALITY 1 "+st+"\033[0;37;40m")
            client.cancel_goal()
            flag = 1
            flag_2 = 0
    
```

If the `active` param is set to a value differrent than 1, the program will at first execute one of if-sections and it will later just idle waiting for `the active` param to get to 1. 


------
## KeyBoard input drive mode: teleop_avoid.py

The script is based on the standard ROS teleop_twist_keyboard.py 

------
## avoidence feature: avoidence.py








