#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp step1-optimistic.lp output.lp"
OUTPUT=FULL-optimistic.txt

cat $FILES > $OUTPUT
