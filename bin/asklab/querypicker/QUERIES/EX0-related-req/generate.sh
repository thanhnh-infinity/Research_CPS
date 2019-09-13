#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp step1-related-req.lp output.lp"
OUTPUT=FULL-related-req.txt

cat $FILES > $OUTPUT
