#! /bin/sh

BASE=../BASE/
FILES="$BASE/step1-BASE.lp $BASE/theory.lp step1-skeptical.lp output.lp"
OUTPUT=FULL-skeptical.txt

cat $FILES > $OUTPUT
