%       -- to be used together with theory*.lp
%          and with step1-BASE.lp

% Reason pessimistically about concerns, i.e. concerns default to unsatisfied
%
% For illustration purposes, we consider as relevant only the following concerns
% and their ancestors:
%  * Confidentiality
%  * Functionality
%  * Integrity
%
% The example shows that, under this reasoning mode, the (relevant portion of the)
% entire concern tree is satisfied. This is due to the fact that the three
% above concerns are addressed by requirements that are satisfied.  

% Enable skeptical inference on concern satisfaction
inference(concerns,pessimistic).


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
