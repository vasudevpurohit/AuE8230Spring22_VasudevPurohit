#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import numpy as np

class TurtleBot:
    #initializing the state of the turtlebot
    def __init__(self):
        rospy.init_node('turtlebot1',anonymous=True)
        
        #initializing the publisher
        self.vel_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
        
        #initializing the subscriber that calls the update pose method
        self.pose_subscribe = rospy.Subscriber('/turtle1/pose',Pose,self.pose_update)
        
        self.pose = Pose()
        self.rate = rospy.Rate(10)
        
    #self_update method that updates the pose of the bot based on its position
    def pose_update(self,data):
        self.pose = data
        self.pose.x = round(self.pose.x,4)
        self.pose.y = round(self.pose.y,4)
        
    #calculates the euclidean distance between the goal pose and the current pose
    def distance(self,goal_pose):
        return sqrt(pow((goal_pose.x-self.pose.x),2)+pow((goal_pose.y-self.pose.y),2))
    
    #calculates the linear speed based on the distance to goal
    def linear_speed(self,goal_pose,const=1.5):
        return const*self.distance(goal_pose)
    
    #calculates the steering angle based on the vector it is supposed to be headed
    def steering_angle(self,goal_pose):
        return atan2((goal_pose.y-self.pose.y),(goal_pose.x-self.pose.x))
    
    #returns the required steering angle based on the difference between the steering angle and the bot orientation
    def angular_vel(self,goal_pose,const=6):
        return const*(self.steering_angle(goal_pose)-self.pose.theta)
    
    def move(self):
        #defining the vertices of the square
        sq_x = np.array([5,8,8,5,5],dtype=float)    #x-coordinates of the square
        sq_y = np.array([5,5,8,8,5],dtype=float)    #y-coordinates of the square
        dist_tolerance = 0.01           #distance tolerance 
        
        goal_pose = Pose()
        vel_msg = Twist()
        
        #first step is to reach the first vertex from the location it spawns
        goal_pose.x = (sq_x[0])
        goal_pose.y = (sq_y[0])
        
        while self.distance(goal_pose) >= dist_tolerance:
            
            #setting the velocities to reach the first vertex
            vel_msg.linear.x = self.linear_speed(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)
            self.vel_publisher.publish(vel_msg)
            self.rate.sleep()
        
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.vel_publisher.publish(vel_msg)
        
        
        #the next step is to align it with the next vertex -- first rotate and then travel along a straight line
        i = 1   #since it has already reached the first vertex
        
        while i < 5:
            goal_pose.x = (sq_x[i])
            goal_pose.y = (sq_y[i])
            diff = abs(self.steering_angle(goal_pose)-self.pose.theta) 
            angle_tolerance = 0.5
            
            t0 = rospy.Time.now().to_sec()
            t1 = rospy.Time.now().to_sec()
            #first rotate the bot to align with the next vertex
            while diff >= angle_tolerance:
                if (t1-t0 <= 4):
                    #setting the velocities to align with the next vertex
                    vel_msg.linear.x = 0
                    vel_msg.linear.y = 0
                    vel_msg.linear.z = 0
                    vel_msg.angular.x = 0
                    vel_msg.angular.y = 0
                    vel_msg.angular.z = self.angular_vel(goal_pose)
                    self.vel_publisher.publish(vel_msg)
                    t1 = rospy.Time.now().to_sec()
                else:
                    break
                        
            
            #set the angular speed to zero once the vertex is aligned
            vel_msg.angular.z = 0
            self.vel_publisher.publish(vel_msg)
            
            current_distance = 0
            t0 = rospy.Time.now().to_sec()
            t1 = rospy.Time.now().to_sec()
            #moving the bot to the next vertex
            while current_distance <= 3:
                if (t1-t0 <= 4):
                    #setting the velocities to reach the first vertex
                    vel_msg.linear.x = self.linear_speed(goal_pose)
                    vel_msg.linear.y = 0
                    vel_msg.linear.z = 0
                    vel_msg.angular.x = 0
                    vel_msg.angular.y = 0
                    vel_msg.angular.z = 0
                    self.vel_publisher.publish(vel_msg)
                    t1 = rospy.Time.now().to_sec()
        		    #calculating the distance travelled
                    current_distance = (vel_msg.linear.x)*(t1-t0)
                else:
                    break
            
            #set the linear speed to zero once the vertex is reached
            vel_msg.linear.x = 0
            self.vel_publisher.publish(vel_msg)
            
            i = i+1
                

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move()
    except rospy.ROSInterruptException:pass
