cmake_minimum_required(VERSION 3.8)
project(jackal_helper)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(Protobuf REQUIRED)
find_package(Boost REQUIRED COMPONENTS system filesystem regex)

# Specify additional locations of header files
include_directories(
  ${GAZEBO_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
  ${PROTOBUF_INCLUDE_DIRS}
)

link_directories(${GAZEBO_LIBRARY_DIRS})

# Declare a C++ executable
add_executable(collision_publisher_node src/collision_publisher.cpp)

# Specify libraries to link a library or executable target against
target_link_libraries(collision_publisher_node
  ${GAZEBO_LIBRARIES}
  ${Boost_LIBRARIES}
  ${PROTOBUF_LIBRARIES}
  pthread
)

# Link against ROS 2 libraries
ament_target_dependencies(
  collision_publisher_node
  rclcpp
  std_msgs
  nav_msgs
  gazebo_ros
)

# Install targets
install(TARGETS
  collision_publisher_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install directories if they exist
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/launch")
  install(DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}
  )
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/worlds")
  install(DIRECTORY worlds
    DESTINATION share/${PROJECT_NAME}
  )
endif()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_lint_cmake_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
