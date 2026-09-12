from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import Goal2D, Pose2D, command_for_pose


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("odom_jsonl", type=Path)
    parser.add_argument("--goal-x", required=True, type=float)
    parser.add_argument("--goal-y", required=True, type=float)
    args = parser.parse_args()
    goal = Goal2D(args.goal_x, args.goal_y)
    for line in args.odom_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        command = command_for_pose(Pose2D(float(value["x_m"]), float(value["y_m"]), float(value["yaw_rad"])), goal)
        print(json.dumps({"stamp": value.get("stamp"), **command.__dict__}, sort_keys=True))


if __name__ == "__main__":
    main()
