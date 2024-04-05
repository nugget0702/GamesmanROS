#!/usr/bin/env python

# Import necessary Python and ROS libraries
import sys
import rospy
from moveit_commander import MoveGroupCommander, roscpp_initialize, roscpp_shutdown
from planning_control.srv import Planning, PlanningResponse

def handle_plan_path(req):
    # Specify the group name of the robot arm. This should match what's defined in your MoveIt setup
    group_name = "robot_arm_group"
    
    # Initialize the MoveGroupCommander for controlling the robot arm
    move_group = MoveGroupCommander(group_name)

    # Get the current joint values of the robot arm
    joint_goal = move_group.get_current_joint_values()

    # Update the joint_goal with the requested joint angles from the service request
    for i, angle in enumerate(req.joint_angles):
        joint_goal[i] = angle

    # Set the updated joint angles as the new target for the robot arm
    move_group.set_joint_value_target(joint_goal)

    # Plan the movement to the new joint angle target
    plan = move_group.plan()

    # Check if the planning was successful
    success = (plan.joint_trajectory.points != [])
    message = "Planning " + ("succeeded" if success else "failed")
    
    # Log the outcome of the planning attempt
    rospy.loginfo(message)

    # Prepare the service response with the planning outcome, message, and planned trajectory
    response = PlanningResponse()
    response.success = success
    response.message = message
    response.trajectory = plan.joint_trajectory

    # Return the response to the service requester
    return response

def planning_server():
    # Initialize the ROS node
    rospy.init_node('planning_server')
    
    # Initialize the MoveIt commander.
    roscpp_initialize(sys.argv)
    
    s = rospy.Service('planning_service', Planning, handle_plan_path)
    
    # Log that the service is ready to receive requests
    rospy.loginfo("Ready to plan path.")
    
    # Keep the service open and listen for requests
    rospy.spin()
    
    # Shutdown the MoveIt commander when the node is stopped
    roscpp_shutdown()

if __name__ == "__main__":
    planning_server()
