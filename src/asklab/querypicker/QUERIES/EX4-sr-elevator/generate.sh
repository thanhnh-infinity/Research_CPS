#! /bin/sh

BASE=../BASE/

REASONING=../Sophisticated-Reasoning/

#FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp"
#OUTPUT=FULL-step1.txt
#cat $FILES > $OUTPUT

#FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp"
#OUTPUT=FULL-step2.txt
#cat $FILES > $OUTPUT

#FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp"
#OUTPUT=FULL-step3.txt
#cat $FILES > $OUTPUT

#FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp $BASE/step3-ext.lp"
#OUTPUT=FULL-step3-ext.txt
#cat $FILES > $OUTPUT


FILES="$REASONING/Integration/SR-RE-01-truthworthiness/ontology_elevator.lp $REASONING/Integration/SR-RE-01-truthworthiness/reasoning_2_1.lp output_sr_re_01_01.lp"
OUTPUT=FULL-step1.txt
cat $FILES > $OUTPUT

FILES="$REASONING/Integration/SR-RE-01-truthworthiness/ontology_elevator.lp $REASONING/Integration/SR-RE-01-truthworthiness/reasoning_2_2.lp output_sr_re_01_02.lp"
OUTPUT=FULL-step2.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp"
OUTPUT=FULL-step3.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp"
OUTPUT=FULL-step4.txt
cat $FILES > $OUTPUT

FILES="$BASE/step1-BASE.lp $BASE/theory.lp $BASE/theory-maxint.lp output.lp $BASE/step1.lp $BASE/step2.lp $BASE/step3.lp $BASE/step3-ext.lp"
OUTPUT=FULL-step4-ext.txt
cat $FILES > $OUTPUT
