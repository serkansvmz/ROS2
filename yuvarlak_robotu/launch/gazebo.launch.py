import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'yuvarlak_robotu'
    gazebo_ros_dir = get_package_share_directory('ros_gz_sim')
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_dir, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    spawn_robot = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-name', 'my_robot', '-file', os.path.join(get_package_share_directory(package_name), 'urdf', 'my_robot.urdf')],
        output='screen',
    )

    return LaunchDescription([gazebo, spawn_robot])
