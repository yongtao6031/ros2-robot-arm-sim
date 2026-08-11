import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from armpy_interfaces.msg import ArmPose


class PoseToJointStatesNode(Node):
    def __init__(self):
        super().__init__('pose_to_joint_states_node')
        self.declare_parameter('upper_len', 0.22)
        self.declare_parameter('forearm_len', 0.18)
        self.declare_parameter('rate', 30.0)
        self.declare_parameter('initial_x', 220)
        self.declare_parameter('initial_y', 80)
        self.declare_parameter('initial_z', 180)
        self.declare_parameter('initial_vel', 2560)

        self.upper_len = self.get_parameter('upper_len').value
        self.forearm_len = self.get_parameter('forearm_len').value
        rate = self.get_parameter('rate').value

        self.pose = ArmPose()
        self.pose.x = self.get_parameter('initial_x').value
        self.pose.y = self.get_parameter('initial_y').value
        self.pose.z = self.get_parameter('initial_z').value
        self.pose.vel = self.get_parameter('initial_vel').value

        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.subscription = self.create_subscription(ArmPose, '/arm/pose', self.pose_callback, 10)
        self.timer = self.create_timer(1.0 / rate, self.publish_joint_states)
        self.get_logger().info('pose_to_joint_states_node ready: /arm/pose -> /joint_states')

    def pose_callback(self, msg):
        self.pose = msg

    @staticmethod
    def clamp(value, lower, upper):
        return max(lower, min(upper, value))

    def pose_to_angles(self):
        target_r = self.clamp(self.pose.x / 1000.0, 0.05, self.upper_len + self.forearm_len - 0.02)
        target_h = self.clamp((self.pose.y - 80) / 1000.0, -0.12, 0.25)
        base_yaw = math.radians(self.pose.z - 180)

        d = (
            target_r * target_r
            + target_h * target_h
            - self.upper_len * self.upper_len
            - self.forearm_len * self.forearm_len
        ) / (2 * self.upper_len * self.forearm_len)
        d = self.clamp(d, -0.95, 0.95)

        elbow = math.acos(d)
        shoulder = math.atan2(target_h, target_r) - math.atan2(
            self.forearm_len * math.sin(elbow),
            self.upper_len + self.forearm_len * math.cos(elbow),
        )
        wrist = -shoulder - elbow
        return [base_yaw, shoulder, elbow, wrist, 0.0]

    def publish_joint_states(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = [
            'base_yaw_joint',
            'shoulder_joint',
            'elbow_joint',
            'wrist_joint',
            'gripper_joint',
        ]
        msg.position = self.pose_to_angles()
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseToJointStatesNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
