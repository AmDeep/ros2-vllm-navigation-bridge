from __future__ import annotations

import json


def main() -> None:
    try:
        import rclpy
        from geometry_msgs.msg import Point, Twist
        from nav_msgs.msg import Odometry
        from rclpy.node import Node
    except ImportError as error:
        raise SystemExit("ROS 2 Python packages are required for ros_node mode") from error

    from .core import Goal2D, Pose2D, command_for_pose

    class NavigationNode(Node):
        def __init__(self) -> None:
            super().__init__("physical_ai_navigation_bridge")
            self.pose = Pose2D(0.0, 0.0, 0.0)
            self.goal: Goal2D | None = None
            self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
            self.create_subscription(Odometry, "/odom", self.on_odom, 10)
            self.create_subscription(Point, "/physical_ai/goal", self.on_goal, 10)
            self.timer = self.create_timer(0.05, self.control)

        def on_odom(self, message: Odometry) -> None:
            self.pose = Pose2D(message.pose.pose.position.x, message.pose.pose.position.y, self.pose.yaw_rad)

        def on_goal(self, message: Point) -> None:
            self.goal = Goal2D(message.x, message.y)

        def control(self) -> None:
            command = command_for_pose(self.pose, self.goal) if self.goal else None
            twist = Twist()
            if command and command.active:
                twist.linear.x = command.linear_x_mps
                twist.angular.z = command.angular_z_rps
            self.publisher.publish(twist)

    rclpy.init()
    node = NavigationNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
