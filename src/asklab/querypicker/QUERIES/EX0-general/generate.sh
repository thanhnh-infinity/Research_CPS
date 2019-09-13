#! /bin/sh

BASE=../BASE/

FILES="$BASE/step1-BASE.lp $BASE/theory.lp output.lp $BASE/step1.lp"
OUTPUT=FULL-step1.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp output.lp $BASE/step1.lp $BASE/step2.lp"
OUTPUT=FULL-step2.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp"
OUTPUT=FULL-step3.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp $BASE/step3-ext.lp"
OUTPUT=FULL-step3-ext.txt
cat $FILES > $OUTPUT
