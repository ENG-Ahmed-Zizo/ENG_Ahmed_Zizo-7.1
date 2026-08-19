from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    background_r = DeclareLaunchArgument('background_r', default_value='69')
    background_g = DeclareLaunchArgument('background_g', default_value='86')
    background_b = DeclareLaunchArgument('background_b', default_value='255')

    cmd_vel_topic_arg = DeclareLaunchArgument('cmd_vel_topic', default_value='/turtle1/cmd_vel')
    color_sensor_topic_arg = DeclareLaunchArgument('color_sensor_topic', default_value='/turtle1/color_sensor')
    dominant_color_topic_arg = DeclareLaunchArgument('dominant_color_topic', default_value='/dominant_color')
    use_stamped_vel_arg = DeclareLaunchArgument('use_stamped_vel', default_value='false')

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        parameters=[{
            'background_r': LaunchConfiguration('background_r'),
            'background_g': LaunchConfiguration('background_g'),
            'background_b': LaunchConfiguration('background_b'),
        }],
    )

    controller_node = Node(
        package='turtle_controller',
        executable='controller_node',
        name='turtle_controller',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'cmd_vel_topic': LaunchConfiguration('cmd_vel_topic'),
            'color_sensor_topic': LaunchConfiguration('color_sensor_topic'),
            'dominant_color_topic': LaunchConfiguration('dominant_color_topic'),
            'use_stamped_vel': LaunchConfiguration('use_stamped_vel'),
        }],
    )

    return LaunchDescription([
        background_r, background_g, background_b,
        cmd_vel_topic_arg, color_sensor_topic_arg, dominant_color_topic_arg, use_stamped_vel_arg,
        turtlesim_node,
        controller_node,
    ])
