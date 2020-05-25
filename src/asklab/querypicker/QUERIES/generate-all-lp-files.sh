#! /bin/sh

DIRS="EX0-general EX0-optimistic EX0-pessimistic EX0-pessimistic-prob \
      EX0-related-req EX0-sake-of-concern EX0-skeptical \
      EX1-camera EX2-laneassist EX3-adaptivecruise EX4-elevator EX4-sr-elevator"

for d in $DIRS
do
	echo "Generating full file in $d..."
	p=`pwd`
	cd "$d"
	./generate.sh
	cd "$p"
done
