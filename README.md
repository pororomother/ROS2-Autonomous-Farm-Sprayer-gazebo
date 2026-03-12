# ROS2 Autonomous Farm Sprayer Gazebo

This repository contains a ROS 2 package for simulating a robot in Ignition Gazebo.

## Modifying the Map
You can change, add, or swap out the 3D farm models by editing the `clean_farm.world` file located inside the `worlds` folder.

## How to Build and Run

To launch the simulation, run the following commands:
   cd ~/ros2_ws
   colcon build --symlink-install --packages-select new_gazebo
   source install/setup.bash
   ros2 launch new_gazebo robot_farm.launch.xml
