%       -- to be used together with theory*.lp
%          and with step1-BASE.lp

% Reason skeptically about concerns, i.e. concerns default to unsatisfied
% but in case of contradictory impacts, from either sub-concerns or
% requirements, the reasoner concludes that the satisfaction of the
% concern is unknown.
%

% For illustration purposes, we consider as relevant only the following concerns
% and their ancestors:
%  * Confidentiality
%  * Functionality
%  * Integrity
%  * ComponentInventory
%
% The ComponentInventory concern is impacted negatively by the requirement to
% use the basic type of the input1 device and impacted positively by
% the requirement to use secure boot on the SAM. (These statements are for 
% illustration only and are not intended to represent any realistic system.)
%
% The example shows that, under this reasoning mode, the (relevant portion of the)
% trustworthiness tree is satisfied. That is due to the fact that the three
% above concerns are addressed by requirements that are satisfied.
% However, it is unknown whether the ComponentInventory is satisfied, due
% to the fact that it is impacted both positively and negatively by requirements.
% The uncertainty is propagated to the ancestors of ComponentInventory: Maintainability
% and Lifecycle.
%

% impact rules -- written in ASP for now since using_basic_input1 is
% a configuration rather than a property and thus is outside of
% the ontology.
% The rule for sec_boot_sam could be encoded in the ontology,
% but we keep it here for uniformity of this example file.
holds(impacted("cpsf:ComponentInventory","cpsf:bc1",neg),S) :-
	step(S),
	holds(sat("using_basic_input1"),S).
holds(impacted("cpsf:ComponentInventory","cpsf:bc1",pos),S) :-
	step(S),
	holds(sat("sec_boot_sam"),S).


% Enable skeptical inference on concern satisfaction
inference(concerns,skeptical).


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
