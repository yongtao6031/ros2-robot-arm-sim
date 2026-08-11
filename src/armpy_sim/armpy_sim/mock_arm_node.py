import rclpy
from rclpy.node import Node

from armpy_interfaces.msg import ArmPose
from armpy_interfaces.srv import ArmPoseRange


class MockArmNode(Node):
    def __init__(self):
        super().__init__('mock_arm_node')
        self.declare_parameter('min_x', 50)
        self.declare_parameter('max_x', 380)
        self.declare_parameter('min_y', -180)
        self.declare_parameter('max_y', 220)
        self.declare_parameter('min_z', 0)
        self.declare_parameter('max_z', 360)

        self.bounds = {
            'x': (self.get_parameter('min_x').value, self.get_parameter('max_x').value),
            'y': (self.get_parameter('min_y').value, self.get_parameter('max_y').value),
            'z': (self.get_parameter('min_z').value, self.get_parameter('max_z').value),
        }

        self.subscription = self.create_subscription(ArmPose, '/arm/pose', self.pose_callback, 10)
        self.range_service = self.create_service(ArmPoseRange, '/arm/pose/range', self.range_callback)
        self.get_logger().info('mock_arm_node ready: no serial port will be opened')

    def check_range(self, x, y, z):
        values = {'x': x, 'y': y, 'z': z}
        for axis, value in values.items():
            lower, upper = self.bounds[axis]
            if value < lower or value > upper:
                return False, f'pose out of range: {axis}={value} not in [{lower}, {upper}]'
        return True, 'pose is in range'

    def pose_callback(self, msg):
        in_range, message = self.check_range(msg.x, msg.y, msg.z)
        if not in_range:
            self.get_logger().warn(message)
        self.get_logger().info(
            f'mock arm received pose: x={msg.x} y={msg.y} z={msg.z} vel={msg.vel}'
        )

    def range_callback(self, request, response):
        response.in_range, response.message = self.check_range(request.x, request.y, request.z)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MockArmNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
