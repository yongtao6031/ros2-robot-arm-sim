from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    start_keyboard = LaunchConfiguration('start_keyboard')
    start_rviz = LaunchConfiguration('start_rviz')

    model_path = PathJoinSubstitution([
        FindPackageShare('armpy_description'),
        'urdf',
        'simple_arm.urdf.xacro',
    ])
    rviz_config = PathJoinSubstitution([
        FindPackageShare('armpy_description'),
        'rviz',
        'armpy_sim.rviz',
    ])
    robot_description = {'robot_description': Command(['xacro ', model_path])}

    return LaunchDescription([
        DeclareLaunchArgument('start_keyboard', default_value='false'),
        DeclareLaunchArgument('start_rviz', default_value='true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[robot_description],
        ),
        Node(
            package='armpy_sim',
            executable='mock_arm_node',
            name='mock_arm_node',
            output='screen',
        ),
        Node(
            package='armpy_sim',
            executable='pose_to_joint_states_node',
            name='pose_to_joint_states_node',
            output='screen',
        ),
        Node(
            condition=IfCondition(start_keyboard),
            package='armpy_sim',
            executable='keyboard_node',
            name='keyboard_node',
            output='screen',
            emulate_tty=True,
        ),
        Node(
            condition=IfCondition(start_rviz),
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
        ),
    ])
