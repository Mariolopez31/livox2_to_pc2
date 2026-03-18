from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="livox2_to_pc2",
            executable="livox2_to_pc2",
            name="livox2_to_pc2",
            output="screen",
            parameters=[{
                "in_topic": "/livox/lidar",
                "out_topic": "/blueboat/livox/points",
                "frame_id": "",
                "include_ring": True,
                "reliability": "best_effort",
            }],
        )
    ])