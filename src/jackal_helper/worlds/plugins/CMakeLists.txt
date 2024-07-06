
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(DynamicModels)

find_package(gazebo REQUIRED)

include_directories(${GAZEBO_INCLUDE_DIRS})
link_directories(${GAZEBO_LIBRARY_DIRS})

add_library(DynamicMale SHARED DynamicMale.cc)
target_link_libraries(DynamicMale ${GAZEBO_LIBRARIES})

add_library(DynamicFemale SHARED DynamicFemale.cc)
target_link_libraries(DynamicFemale ${GAZEBO_LIBRARIES})
