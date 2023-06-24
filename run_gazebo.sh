!#/bin/sh

ign gazebo -s -r --record-path data/manual --record-topic ".*" --log-overwrite gazebo_generated/generated_world.sdf
