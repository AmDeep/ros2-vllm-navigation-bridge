from navigation_bridge.core import Command, Pose2D
from navigation_bridge.isaac_ros_contract import IsaacRosTopics
from navigation_bridge.obstacle_guard import CircularObstacle, guard_command


def test_topic_contract_is_absolute_and_unique() -> None:
    IsaacRosTopics().validate()


def test_obstacle_guard_stops_projected_motion() -> None:
    command = Command(0.3, 0.0, 1.0, True)
    result = guard_command(Pose2D(0.0, 0.0, 0.0), command, [CircularObstacle(0.2, 0.0, 0.1)])
    assert not result.active
    assert result.linear_x_mps == 0.0
