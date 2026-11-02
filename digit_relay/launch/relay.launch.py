
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    nodes = []


    nodes.append(Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
    ))


    for i in range(1, 7):
        nodes.append(Node(
            package='digit_relay',
            executable=f'member{i}',
            name=f'member{i}',
            output='screen',
        ))

    return LaunchDescription(nodes)
