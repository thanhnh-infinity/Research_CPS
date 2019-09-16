#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp step1-pessimistic.lp output.lp"
OUTPUT=FULL-pessimistic.txt

cat $FILES > $OUTPUT
