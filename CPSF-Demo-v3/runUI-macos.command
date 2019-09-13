#! /bin/sh
#
D="`dirname $0`"
if [ -z "$D" ]; then
        D="`pwd`"
fi
cd "$D"
chmod 0755 asklab/cpsf/dlv/dlv-macosx asklab/cpsf/mkatoms/mkatoms-macosx asklab/cpsf/clingo-4.4.0/clingo-macosx
java asklab.ui.ReasonerUI
