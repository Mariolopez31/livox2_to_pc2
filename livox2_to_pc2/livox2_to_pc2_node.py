#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

from livox_ros_driver2.msg import CustomMsg
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2


def _rel(s: str) -> ReliabilityPolicy:
    s = (s or "").strip().lower()
    return ReliabilityPolicy.RELIABLE if s == "reliable" else ReliabilityPolicy.BEST_EFFORT


class Livox2ToPC2(Node):
    def __init__(self):
        super().__init__("livox2_to_pc2")

        self.declare_parameter("in_topic", "/stonefish_ros2/blueboat/livox")
        self.declare_parameter("out_topic", "/blueboat/livox/points")
        self.declare_parameter("sub_reliability", "reliable")     # reliable | best_effort
        self.declare_parameter("pub_reliability", "reliable")  # reliable | best_effort
        self.declare_parameter("frame_id", "")                    # si vacío, usa msg.header.frame_id
        self.declare_parameter("include_ring", True)

        in_topic = self.get_parameter("in_topic").value
        out_topic = self.get_parameter("out_topic").value
        self.frame_id_override = self.get_parameter("frame_id").value
        self.include_ring = bool(self.get_parameter("include_ring").value)

        sub_rel = str(self.get_parameter("sub_reliability").value)
        pub_rel = str(self.get_parameter("pub_reliability").value)

        sub_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            reliability=_rel(sub_rel),
            durability=DurabilityPolicy.VOLATILE,
        )

        pub_qos = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=5,
            reliability=_rel(pub_rel),
            durability=DurabilityPolicy.VOLATILE,
        )

        self.sub = self.create_subscription(CustomMsg, in_topic, self.cb, sub_qos)
        self.pub = self.create_publisher(PointCloud2, out_topic, pub_qos)

        # Campos
        if self.include_ring:
            self.fields = [
                PointField(name="x", offset=0,  datatype=PointField.FLOAT32, count=1),
                PointField(name="y", offset=4,  datatype=PointField.FLOAT32, count=1),
                PointField(name="z", offset=8,  datatype=PointField.FLOAT32, count=1),
                PointField(name="intensity", offset=12, datatype=PointField.FLOAT32, count=1),
                PointField(name="ring", offset=16, datatype=PointField.UINT16,  count=1),
            ]
        else:
            self.fields = [
                PointField(name="x", offset=0,  datatype=PointField.FLOAT32, count=1),
                PointField(name="y", offset=4,  datatype=PointField.FLOAT32, count=1),
                PointField(name="z", offset=8,  datatype=PointField.FLOAT32, count=1),
                PointField(name="intensity", offset=12, datatype=PointField.FLOAT32, count=1),
            ]

        self.get_logger().info(
            f"Sub: {in_topic} ({sub_rel.lower()}) -> Pub: {out_topic} ({pub_rel.lower()})"
        )

    def cb(self, msg: CustomMsg):
        frame_id = self.frame_id_override if self.frame_id_override else msg.header.frame_id

        if self.include_ring:
            points_iter = ((p.x, p.y, p.z, float(p.reflectivity), int(p.line)) for p in msg.points)
        else:
            points_iter = ((p.x, p.y, p.z, float(p.reflectivity)) for p in msg.points)

        pc_msg = pc2.create_cloud(msg.header, self.fields, points_iter)
        pc_msg.header.frame_id = frame_id
        self.pub.publish(pc_msg)


def main():
    rclpy.init()
    node = Livox2ToPC2()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()