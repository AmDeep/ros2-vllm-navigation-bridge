from navigation_bridge.core import Goal2D, Pose2D, command_for_pose


def test_goal_stops_robot() -> None:
    command = command_for_pose(Pose2D(1.0, 1.0, 0.0), Goal2D(1.0, 1.0))
    assert not command.active
    assert command.linear_x_mps == 0.0


def test_command_is_bounded() -> None:
    command = command_for_pose(Pose2D(0.0, 0.0, 0.0), Goal2D(10.0, 10.0))
    assert 0 <= command.linear_x_mps <= 0.45
    assert abs(command.angular_z_rps) <= 1.2
