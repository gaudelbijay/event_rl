// src/collision_publisher.cpp

#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/gazebo_client.hh>
#include <gazebo/gazebo_config.h>
#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/bool.hpp>
#include <iostream>
#include <vector>

rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr pub;
bool airborne;
const std::string DELIMITER = "::";

// Forces callback function
void forcesCb(ConstContactsPtr &_msg){
    // What to do when callback
    for (int i = 0; i < _msg->contact_size(); ++i) {
        std::string entity1 = _msg->contact(i).collision1();
        entity1 = entity1.substr(0, entity1.find(DELIMITER)); // Extract entity1 name

        std::string entity2 = _msg->contact(i).collision2();
        entity2 = entity2.substr(0, entity2.find(DELIMITER)); // Extract entity1 name

        if(entity1 != "ground_plane" && entity2 != "ground_plane"){
            if (entity1 == "jackal" || entity2 == "jackal"){
                std_msgs::msg::Bool collide;
                collide.data = true;
                pub->publish(collide);
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "%s:%s", entity1.c_str(), entity2.c_str());
                return;
            }
        }
    }
}

// Position callback function
void positionCb(const nav_msgs::msg::Odometry::SharedPtr msg2){
    if (msg2->pose.pose.position.z > 0.3) {
        airborne = true;
    } else {
        airborne = false;
    }
}

int main(int argc, char **argv){
    // Set variables
    airborne = false;

    // Load Gazebo
    gazebo::client::setup(argc, argv);

    // Create ROS 2 node and init
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("force_measure");

    // Create ROS 2 publisher
    pub = node->create_publisher<std_msgs::msg::Bool>("collision", 10);

    // Create Gazebo node and init
    gazebo::transport::NodePtr gz_node(new gazebo::transport::Node());
    gz_node->Init();

    // Listen to Gazebo contacts topic
    auto sub = gz_node->Subscribe("/gazebo/default/physics/contacts", forcesCb);

    // Listen to ROS 2 for position
    auto sub2 = node->create_subscription<nav_msgs::msg::Odometry>("ground_truth/state", 10, positionCb);

    // Busy wait loop...replace with your own code as needed.
    rclcpp::WallRate loop_rate(10);
    while (rclcpp::ok())
    {
        gazebo::common::Time::MSleep(100);

        // Spin ROS (needed for publisher and subscribers-calling callbacks)
        rclcpp::spin_some(node);

        // Sleep to maintain the loop rate
        loop_rate.sleep();
    }

    // Make sure to shut everything down.
    gazebo::client::shutdown();
    rclcpp::shutdown();
}
