import random
import argparse
import os

def generate_sdf(filename, directory, num_objects, range_min, range_max):
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

    with open(filepath, "w") as file:
        file.write("""<?xml version='1.0' encoding='ASCII'?>
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
        
        file.write("""
  </world>
</sdf>
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an SDF file with random boxes and cylinders.")
    parser.add_argument("--filename", type=str, required=True, help="Name of the SDF file to generate.")
    parser.add_argument("--directory", type=str, required=True, help="Directory to save the SDF file.")
    parser.add_argument("--num_objects", type=int, default=100, help="Total number of boxes and cylinders to generate.")
    parser.add_argument("--range_min", type=float, default=-10.0, help="Minimum range for the positions.")
    parser.add_argument("--range_max", type=float, default=10.0, help="Maximum range for the positions.")
    
    args = parser.parse_args()
    generate_sdf(args.filename, args.directory, args.num_objects, args.range_min, args.range_max)
