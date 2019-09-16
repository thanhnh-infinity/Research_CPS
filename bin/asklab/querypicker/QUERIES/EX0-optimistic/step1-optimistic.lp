%       -- to be used together with theory*.lp
%          and with step1-BASE.lp

% Reason optimistically about concerns, concerns default to unsatisfied,
% but concerns that have no requirements nor sub-concerns are vacuously
% satisfied.
%
% The example shows that, under this reasoning mode, the entire concern
% tree is satisfied.

% Enable optimistic inference on concern satisfaction
inference(concerns,optimistic).

% ------ Output Interface ------

output(D,property,"-",S) :- last_step(S), holds(sat(A),S), atomic_statement(P,A), descr(P,D).
output(C,concern,F,S) :- last_step(S), holds(sat(C,F),S),concern(C),not aspect(C), C!=all.
output(C,aspect,F,S) :- last_step(S), holds(sat(C,F),S),aspect(C).
output("concern-tree",tree,F,S) :- last_step(S), holds(sat(all,F),S).

output(C,"concern/aspect (unk)",F,S) :- 
	inference(concerns,skeptical),
	last_step(S), concern(C), relevantToFunc(C,F), 
	not holds(sat(C,F),S),
	not holds(sat(C,F),S).

output_headings("satisfied concern/aspect/property","type","function","step").
