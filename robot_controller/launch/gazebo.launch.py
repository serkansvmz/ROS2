import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'robot_controller'
    
    # 1. Gazebo'yu başlat
    gazebo_ros_dir = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items(),
    )

    # 2. Robotu Gazebo'ya ekle (Spawn)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_robot',
            '-file', os.path.join(get_package_share_directory(package_name), 'urdf', 'my_robot.urdf')
        ],
        output='screen',
    )

    # 3. İletişim Köprüsü (Bridge) - Otomatik başlar
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
        output='screen'
    )

    # 4. Senin Hareket Kodun (5 saniye gecikmeyle başlar, Gazebo'nun açılmasını bekler)
    move_robot = TimerAction(
        period=5.0,
        actions=[
            Node(
                package=package_name,
                executable='move_robot',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gazebo,
        spawn_robot,
        bridge,
        move_robot
    ])
