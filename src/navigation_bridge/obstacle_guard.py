from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from .core import Command, Pose2D


@dataclass(frozen=True)
class CircularObstacle:
    x_m: float
    y_m: float
    radius_m: float


def guard_command(pose: Pose2D, command: Command, obstacles: list[CircularObstacle], robot_radius_m: float = 0.25, lookahead_m: float = 0.6) -> Command:
    if not command.active:
        return command
    projected_x = pose.x_m + min(lookahead_m, command.linear_x_mps) 
    projected_y = pose.y_m
    for obstacle in obstacles:
        if hypot(projected_x - obstacle.x_m, projected_y - obstacle.y_m) <= robot_radius_m + obstacle.radius_m:
            return Command(0.0, 0.0, command.distance_m, False)
    return command
