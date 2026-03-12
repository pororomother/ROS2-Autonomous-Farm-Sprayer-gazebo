import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'new_gazebo'
    pkg_share = get_package_share_directory(pkg_name)

    # =======================================================
    # 1. Tell Ignition where your old 3D models are saved!
    # (THIS MUST HAPPEN FIRST)
    # =======================================================
   
    farm_models_path = os.path.expanduser('~/farm2/models')    

    set_ign_path = SetEnvironmentVariable(
        name='IGN_GAZEBO_RESOURCE_PATH',
        value=[farm_models_path, ':', os.path.join(pkg_share, 'worlds'), ':', os.path.join(pkg_share, 'models')]
    )
    
    set_sdf_path = SetEnvironmentVariable(
        name='SDF_PATH',
        value=farm_models_path
    )

    # 2. Process the URDF file
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    robot_urdf = xacro.process_file(xacro_file).toxml()

    # 3. Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_urdf, 'use_sim_time': True}]
    )

    # 4. Start Ignition Gazebo (Fortress) and load the world
    world_file = os.path.join(pkg_share, 'worlds', 'clean_farm.world')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world_file}'}.items() # The -r flag tells it to run (unpaused)
    )

    # 5. Spawn the Robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'ranger1s_sprayer',
            '-string', robot_urdf,
            '-x', '-2.05',
            '-y', '-1.2',
            '-z', '0.3',       
            '-Y', '1.5708'     
        ],
        output='screen'
    )

    # =======================================================
    # 6. THE BRIDGE: Translating between Ignition and ROS 2
    # =======================================================
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock (Ignition -> ROS 2)
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            # Velocity commands (ROS 2 -> Ignition)
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            # Odometry (Ignition -> ROS 2)
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            # Camera Image (Ignition -> ROS 2)
            '/zed/image_raw@sensor_msgs/msg/Image[ignition.msgs.Image',
        ],
        output='screen'
    )

    # 7. Automatically open the Camera Viewer
    rqt_image_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        arguments=['/zed/image_raw'],
        output='screen'
    )

    return LaunchDescription([
        set_ign_path,
        set_sdf_path,  
        robot_state_publisher_node,
        gz_sim,
        spawn_entity,
        bridge,
        rqt_image_node
    ])