from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    sync_queue_size = LaunchConfiguration('sync_queue_size')
    topic_queue_size = LaunchConfiguration('topic_queue_size')

    return LaunchDescription([

        DeclareLaunchArgument(
            name='use_sim_time', default_value='true',
            description='Use simulation time if true'
        ),

        DeclareLaunchArgument(
            name='scanner', default_value='',
            description='Namespace for sample topics'
        ),

        DeclareLaunchArgument(
            name='sync_queue_size', default_value='10',
            description='Sync queue size for synchronized topics'
        ),

        DeclareLaunchArgument(
            name='topic_queue_size', default_value='20',
            description='Queue size for input topics'
        ),

        # Node(
        #     package='pointcloud_to_laserscan', executable='dummy_pointcloud_publisher',
        #     remappings=[('cloud', [LaunchConfiguration(variable_name='scanner'), '/camera/points'])],
        #     parameters=[{'cloud_frame_id': 'cloud', 'cloud_extent': 2.0, 'cloud_size': 500}],
        #     name='cloud_publisher'
        # ),
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_transform_publisher',
        #     arguments=[
        #         '--x', '0', '--y', '0', '--z', '0',
        #         '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
        #         '--frame-id', 'map', '--child-frame-id', 'cloud'
        #     ]
        # ),
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in', [LaunchConfiguration(variable_name='scanner'), '/camera/points']),
                        ('scan', [LaunchConfiguration(variable_name='scanner'), '/camera/scan'])],
            parameters=[{
                'target_frame': 'base_scan',
                'transform_tolerance': 0.01,
                'min_height': 0.0,
                'max_height': 0.16,
                'angle_min': -1.5708,  # -M_PI/2
                'angle_max': 1.5708,  # M_PI/2
                'angle_increment': 0.0087,  # M_PI/360.0
                'scan_time': 0.03333,
                'range_min': 0.45,
                'range_max': 10.0,
                'use_inf': True,
                'inf_epsilon': 1.0,
                'use_sim_time': use_sim_time,
                'sync_queue_size': sync_queue_size,  # 동기화 큐 크기
                'topic_queue_size': topic_queue_size
                
            }],
            name='pointcloud_to_laserscan'
        )
    ])
