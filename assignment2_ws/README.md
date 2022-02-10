## Package included:
-tb_sim - TurtleBot simulator\
\
## Scripts included
-circle.py -- moves the turlebot in a circle with a constant twist velocity\
The linear velocity along x and angular velocity about z are input by the user.\
![](https://github.com/vasudevpurohit/AuE8230Spring22_VasudevPurohit/blob/master/assignment2_ws/videos/circle.gif)

-square_openloop.py -- moves the turtlebot in a square using open loop control\
Here, the speed is hardcoded but can also be passed as an input by the user.\
![](https://github.com/vasudevpurohit/AuE8230Spring22_VasudevPurohit/blob/master/assignment2_ws/videos/square_openloop.gif)

-square_closedloop.py -- moves the turtlebot in a square using closed loop control\
The velocity is decided by a turtlebot_controller, that changes the linear and angular speed based on closeness to the goal pose. A time-based break has also been included to prevent the controller from giving infinitesimally small speed inputs to reach the goal pose.
![](https://github.com/vasudevpurohit/AuE8230Spring22_VasudevPurohit/blob/master/assignment2_ws/videos/square_closedloop.gif)

## Running the files
(i) Launch the ROS master node\
(ii) Launch the turtlesim node\
(iii) pass the command - source devel/setup.bash and use standard ROS commands to run above scripts (rosrun <package_name> <script.py>)
