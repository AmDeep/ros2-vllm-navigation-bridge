from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IsaacRosTopics:
    """Deployment-configurable ROS 2 topic names for an Isaac ROS graph."""

    odometry: str = "/odom"
    camera_left: str = "/left/image_rect"
    camera_right: str = "/right/image_rect"
    depth: str = "/depth/image_rect"
    cmd_vel: str = "/cmd_vel"

    def validate(self) -> None:
        names = (self.odometry, self.camera_left, self.camera_right, self.depth, self.cmd_vel)
        if any(not name.startswith("/") for name in names):
            raise ValueError("ROS 2 topic names must be absolute")
        if len(set(names)) != len(names):
            raise ValueError("navigation topics must be distinct")
