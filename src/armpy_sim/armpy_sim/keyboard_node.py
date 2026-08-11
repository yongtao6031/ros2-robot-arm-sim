import select
import sys
import termios
import tty

import rclpy
from rclpy.node import Node

from armpy_interfaces.msg import ArmPose
from armpy_interfaces.srv import ArmPoseRange


HELP = """
Keyboard control:
  W/S: increase/decrease x
  Q/E: increase/decrease y
  A/D: increase/decrease z
  C: quit
"""


class KeyboardNode(Node):
    def __init__(self):
        super().__init__('keyboard_node')
        self.declare_parameter('initial_x', 220)
        self.declare_parameter('initial_y', 80)
        self.declare_parameter('initial_z', 180)
        self.declare_parameter('initial_vel', 2560)
        self.declare_parameter('step', 5)
        self.declare_parameter('use_range_service', True)

        self.pose = ArmPose()
        self.pose.x = self.get_parameter('initial_x').value
        self.pose.y = self.get_parameter('initial_y').value
        self.pose.z = self.get_parameter('initial_z').value
        self.pose.vel = self.get_parameter('initial_vel').value
        self.step = self.get_parameter('step').value
        self.use_range_service = self.get_parameter('use_range_service').value

        self.publisher = self.create_publisher(ArmPose, '/arm/pose', 10)
        self.range_client = self.create_client(ArmPoseRange, '/arm/pose/range')

    def read_key(self):
        settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if ready:
                return sys.stdin.read(1).lower()
            return ''
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def update_pose(self, key):
        if key == 'w':
            self.pose.x += self.step
        elif key == 's':
            self.pose.x -= self.step
        elif key == 'q':
            self.pose.y += self.step
        elif key == 'e':
            self.pose.y -= self.step
        elif key == 'a':
            self.pose.z += self.step
        elif key == 'd':
            self.pose.z -= self.step
        else:
            return False
        return True

    def pose_in_range(self):
        if not self.use_range_service:
            return True
        if not self.range_client.wait_for_service(timeout_sec=0.05):
            self.get_logger().warn('range service unavailable, publishing without remote range check')
            return True

        request = ArmPoseRange.Request()
        request.x = self.pose.x
        request.y = self.pose.y
        request.z = self.pose.z
        future = self.range_client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=0.3)
        if not future.done() or future.result() is None:
            self.get_logger().warn('range service timed out, publishing without remote range check')
            return True

        response = future.result()
        if not response.in_range:
            self.get_logger().warn(response.message)
        return response.in_range

    def publish_pose(self):
        if not self.pose_in_range():
            return
        self.publisher.publish(self.pose)
        self.get_logger().info(
            f'published pose: x={self.pose.x} y={self.pose.y} '
            f'z={self.pose.z} vel={self.pose.vel}'
        )

    def run(self):
        print(HELP)
        self.publish_pose()
        while rclpy.ok():
            key = self.read_key()
            if key == 'c':
                self.get_logger().info('keyboard control stopped')
                break
            if self.update_pose(key):
                self.publish_pose()
            rclpy.spin_once(self, timeout_sec=0.0)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
