import random
import argparse
import os

def generate_sdf(filename, directory, num_objects, range_min, range_max, num_male, num_female, num_chair, num_table):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)

    positions = set()

    def generate_random_position():
        while True:
            x = random.uniform(range_min, range_max)
            y = random.uniform(range_min, range_max)
            if (-0.5 <= x <= 0.5) and (-0.5 <= y <= 0.5):
                continue
            pos = (round(x, 2), round(y, 2))
            if pos not in positions:
                positions.add(pos)
                return pos

    def generate_plugin_code(name):
        return f"""
#include <gazebo/gazebo.hh>
#include <ignition/math.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>

namespace gazebo
{{
  class {name} : public ModelPlugin
  {{
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {{
      this->model = _parent;

      gazebo::common::PoseAnimationPtr anim(
          new gazebo::common::PoseAnimation("{name}", 10.0, true));

      gazebo::common::PoseKeyFrame *key;

      key = anim->CreateKeyFrame(0.0);
      key->Translation(ignition::math::Vector3d(0, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      key = anim->CreateKeyFrame(5.0);
      key->Translation(ignition::math::Vector3d(3, 3, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 1.57));

      key = anim->CreateKeyFrame(10.0);
      key->Translation(ignition::math::Vector3d(0, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 3.14));

      this->model->SetAnimation(anim);
    }}

    private: physics::ModelPtr model;
  }};

  GZ_REGISTER_MODEL_PLUGIN({name})
}}
"""

    # Create plugin directory if it doesn't exist
    plugin_directory = os.path.join(directory, "plugins")
    if not os.path.exists(plugin_directory):
        os.makedirs(plugin_directory)

    # Generate plugin code files
    plugin_names = ["DynamicMale", "DynamicFemale"]
    for plugin_name in plugin_names:
        plugin_code = generate_plugin_code(plugin_name)
        with open(os.path.join(plugin_directory, f"{plugin_name}.cc"), "w") as f:
            f.write(plugin_code)

    # Generate CMakeLists.txt file
    cmakelists_content = f"""
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(DynamicModels)

find_package(gazebo REQUIRED)

include_directories(${{GAZEBO_INCLUDE_DIRS}})
link_directories(${{GAZEBO_LIBRARY_DIRS}})

add_library(DynamicMale SHARED DynamicMale.cc)
target_link_libraries(DynamicMale ${{GAZEBO_LIBRARIES}})

add_library(DynamicFemale SHARED DynamicFemale.cc)
target_link_libraries(DynamicFemale ${{GAZEBO_LIBRARIES}})
"""
    with open(os.path.join(plugin_directory, "CMakeLists.txt"), "w") as f:
        f.write(cmakelists_content)

    with open(filepath, "w") as file:
        file.write("""<?xml version='1.0' encoding='UTF-8'?>
<sdf version='1.7'>
  <world name='warehouse'>
    <physics type="ode">
      <max_step_size>0.003</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin name='ignition::gazebo::systems::Physics' filename='libignition-gazebo-physics-system.so'/>
    <plugin name='ignition::gazebo::systems::UserCommands' filename='libignition-gazebo-user-commands-system.so'/>
    <plugin name='ignition::gazebo::systems::SceneBroadcaster' filename='libignition-gazebo-scene-broadcaster-system.so'/>
    <plugin name="ignition::gazebo::systems::Sensors" filename="libignition-gazebo-sensors-system.so">
      <render_engine>ogre2</render_engine>
    </plugin>
    <plugin name="ignition::gazebo::systems::Imu" filename="libignition-gazebo-imu-system.so"/>
    <plugin name="ignition::gazebo::systems::NavSat" filename="libignition-gazebo-navsat-system.so"/>

    <scene>
      <ambient>1 1 1 1</ambient>
      <background>0 0 0 1</background>
      <shadows>0</shadows>
      <grid>false</grid>
    </scene>

    <spherical_coordinates>
      <surface_model>EARTH_WGS84</surface_model>
      <world_frame_orientation>ENU</world_frame_orientation>
      <latitude_deg>-22.986687</latitude_deg>
      <longitude_deg>-43.202501</longitude_deg>
      <elevation>0</elevation>
      <heading_deg>0</heading_deg>
    </spherical_coordinates>

    <model name='ground_plane'>
      <static>true</static>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <plane>
              <normal>0.0 0.0 1</normal>
              <size>1 1</size>
            </plane>
          </geometry>
        </collision>
      </link>
      <pose>0 0 0 0 0 0</pose>
    </model>
""")

        for i in range(num_objects):
            box_pos = generate_random_position()
            cylinder_pos = generate_random_position()
            box_pose = f"{box_pos[0]} {box_pos[1]} 0 0 0 0"
            cylinder_pose = f"{cylinder_pos[0]} {cylinder_pos[1]} 0 0 0 0"
            box_color = f"{random.random()} {random.random()} {random.random()} 1"
            cylinder_color = f"{random.random()} {random.random()} {random.random()} 1"

            file.write(f"""
    <model name='unit_box_{i}'>
      <static>true</static>
      <pose>{box_pose}</pose>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <box>
              <size>0.450000 0.450000 0.450000</size>
            </box>
          </geometry>
          <max_contacts>10</max_contacts>
        </collision>
        <visual name='visual'>
          <geometry>
            <box>
              <size>0.450000 0.450000 0.450000</size>
            </box>
          </geometry>
          <material>
            <ambient>{box_color}</ambient>
            <diffuse>{box_color}</diffuse>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/RandomColor{i}</name>
            </script>
          </material>
        </visual>
      </link>
    </model>

    <model name='unit_cylinder_{i}'>
      <static>true</static>
      <pose>{cylinder_pose}</pose>
      <link name='link'>
        <collision name='collision'>
          <geometry>
            <cylinder>
              <radius>0.085000</radius>
              <length>1.000000</length>
            </cylinder>
          </geometry>
          <max_contacts>10</max_contacts>
        </collision>
        <visual name='visual'>
          <geometry>
            <cylinder>
              <radius>0.085000</radius>
              <length>1.000000</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>{cylinder_color}</ambient>
            <diffuse>{cylinder_color}</diffuse>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/RandomColor{i}</name>
            </script>
          </material>
        </visual>
      </link>
    </model>
""")

        for i in range(num_male):
            male_pos = generate_random_position()
            male_pose = f"{male_pos[0]} {male_pos[1]} 0 0 0 {random.uniform(0, 3.14)}"
            file.write(f"""
    <include>
      <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/MaleVisitorOnPhone</uri>
      <name>MaleVisitor_{i}</name>
      <pose>{male_pose}</pose>
      <plugin name='MalePlugin{i}' filename='libDynamicMale.so'/>
    </include>
""")

        for i in range(num_female):
            female_pos = generate_random_position()
            female_pose = f"{female_pos[0]} {female_pos[1]} 0 0 0 {random.uniform(0, 3.14)}"
            file.write(f"""
    <include>
      <uri>https://fuel.gazebosim.org/1.0/plateau/models/Casual female</uri>
      <name>CasualFemale_{i}</name>
      <pose>{female_pose}</pose>
      <plugin name='FemalePlugin{i}' filename='libDynamicFemale.so'/>
    </include>
""")
            
        for i in range(num_chair):
            chair_pose = generate_random_position()
            chair_pose = f"{chair_pose[0]} {chair_pose[1]} 0 0 0 {random.uniform(0, 3.14)}"
            file.write(f"""
    <include>
      <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Chair</uri>
      <name>Chair{i}</name>
      <pose>{chair_pose}</pose>
    </include>
""")

        for i in range(num_table):
            table_pos = generate_random_position()
            table_pose = f"{table_pos[0]} {table_pos[1]} 0 0 0 {random.uniform(0, 3.14)}"
            file.write(f"""
    <include>
      <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Table</uri>
      <name>Table{i}</name>
      <pose>{table_pose}</pose>
    </include>
""")

        file.write("""
  </world>
</sdf>
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an SDF file with random boxes, cylinders, and people models.")
    parser.add_argument("--filename", type=str, required=True, help="Name of the SDF file to generate.")
    parser.add_argument("--directory", type=str, required=True, help="Directory to save the SDF file.")
    parser.add_argument("--num_objects", type=int, default=100, help="Total number of boxes and cylinders to generate.")
    parser.add_argument("--range_min", type=float, default=-15.0, help="Minimum range for the positions.")
    parser.add_argument("--range_max", type=float, default=15.0, help="Maximum range for the positions.")
    parser.add_argument("--num_male", type=int, default=15, help="Number of male models to generate.")
    parser.add_argument("--num_female", type=int, default=15, help="Number of female models to generate.")
    parser.add_argument("--num_chair", type=int, default=20, help="Number of chair models to generate.")
    parser.add_argument("--num_table", type=int, default=20, help="Number of table models to generate.")
    
    args = parser.parse_args()
    generate_sdf(args.filename, args.directory, args.num_objects, args.range_min, args.range_max, args.num_male, args.num_female, args.num_chair, args.num_table)
