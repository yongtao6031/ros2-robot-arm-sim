import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from visualization_msgs.msg import Marker, MarkerArray


class SceneMarkerNode(Node):
    def __init__(self):
        super().__init__('scene_marker_node')
        qos = QoSProfile(depth=1)
        qos.reliability = ReliabilityPolicy.RELIABLE
        qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        self.publisher = self.create_publisher(MarkerArray, '/armpy_scene', qos)
        self.timer = self.create_timer(1.0, self.publish_scene)
        self.get_logger().info('scene_marker_node ready: publishing /armpy_scene')

    @staticmethod
    def make_marker(marker_id, marker_type, position, scale, color):
        marker = Marker()
        marker.header.frame_id = 'base_link'
        marker.ns = 'scene'
        marker.id = marker_id
        marker.type = marker_type
        marker.action = Marker.ADD
        marker.pose.position.x = position[0]
        marker.pose.position.y = position[1]
        marker.pose.position.z = position[2]
        marker.pose.orientation.w = 1.0
        marker.scale.x = scale[0]
        marker.scale.y = scale[1]
        marker.scale.z = scale[2]
        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]
        return marker

    def publish_scene(self):
        now = self.get_clock().now().to_msg()
        markers = MarkerArray()

        markers.markers.append(self.make_marker(
            0,
            Marker.SPHERE,
            (0.30, 0.12, 0.035),
            (0.07, 0.07, 0.07),
            (0.95, 0.18, 0.12, 1.0),
        ))

        box_color = (0.15, 0.45, 0.95, 0.55)
        markers.markers.extend([
            self.make_marker(1, Marker.CUBE, (0.20, -0.22, 0.005), (0.18, 0.14, 0.01), box_color),
            self.make_marker(2, Marker.CUBE, (0.20, -0.295, 0.045), (0.18, 0.01, 0.08), box_color),
            self.make_marker(3, Marker.CUBE, (0.20, -0.145, 0.045), (0.18, 0.01, 0.08), box_color),
            self.make_marker(4, Marker.CUBE, (0.105, -0.22, 0.045), (0.01, 0.14, 0.08), box_color),
            self.make_marker(5, Marker.CUBE, (0.295, -0.22, 0.045), (0.01, 0.14, 0.08), box_color),
        ])

        for marker in markers.markers:
            marker.header.stamp = now

        self.publisher.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = SceneMarkerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
