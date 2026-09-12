from __future__ import annotations

from dataclasses import dataclass
from math import atan2, hypot


@dataclass(frozen=True)
class Pose2D:
    x_m: float
    y_m: float
    yaw_rad: float


@dataclass(frozen=True)
class Goal2D:
    x_m: float
    y_m: float
    tolerance_m: float = 0.12


@dataclass(frozen=True)
class Command:
    linear_x_mps: float
    angular_z_rps: float
    distance_m: float
    active: bool


def command_for_pose(pose: Pose2D, goal: Goal2D, max_linear: float = 0.45, max_angular: float = 1.2) -> Command:
    dx, dy = goal.x_m - pose.x_m, goal.y_m - pose.y_m
    distance = hypot(dx, dy)
    if distance <= goal.tolerance_m:
        return Command(0.0, 0.0, distance, False)
    heading_error = atan2(dy, dx) - pose.yaw_rad
    while heading_error > 3.141592653589793:
        heading_error -= 2 * 3.141592653589793
    while heading_error < -3.141592653589793:
        heading_error += 2 * 3.141592653589793
    linear = min(max_linear, 0.8 * distance) * max(0.0, 1.0 - abs(heading_error) / 1.57)
    angular = max(-max_angular, min(max_angular, 2.0 * heading_error))
    return Command(linear, angular, distance, True)
