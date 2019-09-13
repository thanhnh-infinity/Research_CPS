#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp step1-sake-of-concern.lp output.lp"
OUTPUT=FULL-sake-of-concern.txt

cat $FILES > $OUTPUT
