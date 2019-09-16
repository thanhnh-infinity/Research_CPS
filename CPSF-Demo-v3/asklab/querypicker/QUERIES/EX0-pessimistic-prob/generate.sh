#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-prob.lp step1-pessimistic-prob.lp output.lp"
OUTPUT=FULL-pessimistic.txt

cat $FILES > $OUTPUT
