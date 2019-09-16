%%%%% NOTE: to use inference on the satisfaction of concerns,
%%%%%       one MUST define one of the following facts:
%%%%%
%%%%%         inference(concerns,pessimistic)
%%%%%         inference(concerns,skeptical)
%%%%%         inference(concerns,optimistic)


% ------ Input Interface ------

property(P) :- input(P,"rdf:type","cpsf:Property").
descr(P,D) :- input(P,"rdfs:comment",D).
atomic_statement(P,A) :- input(P,"cpsf:atomicStatement",A).
isAssertion(P) :- input(P,"cpsf:hasType","cpsf:PropertyType_Assertion").
concern(C) :- input(C,"rdf:type","cpsf:Concern").
aspect(A) :- input(A,"rdf:type","cpsf:Aspect").
subconcern(S,O) :- input(S,"cpsf:includesConcern",O).

% every aspect is a concern
concern(A) :- aspect(A).

% meta-aspect "all", which is a parent of every aspect
concern(all).
subconcern(all,A) :-
	aspect(A).

% TO BE CHANGED IN ONTOLOGY <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 
% --- not needed ---
%%addressedBy(C,P) :- input(C,"cpsf:addressedByProperty",P).
%addresses(A,C,F) :- 
%	input(P,"cpsf:addresses",C),
%	input(P,"cpsf:addressesAtFunc",F),
%	atomic_statement(P,A),
%	isAssertion(P).
	


nextFC(F1,F2) :- input(F2,"cpsf:nextFC",F1).
% Auxiliary relation isFunctionClass
isFunctionClass(F1) :- nextFC(F1,F2).
isFunctionClass(F2) :- nextFC(F1,F2).
functionClass(F,FC) :- isFunctionClass(FC), input(F,"rdf:type",FC).
refinedInto(F1,F2) :- input(F1,"cpsf:refinedInto",F2).
hasBC(APP,BC) :- input(APP,"cpsf:hasBC",BC).
relevantToFunc(C,F) :- input(C,"cpsf:relevantToFunc",F).

% a concern is relevant to F if a sub-concern is relevant to F  
relevantToFunc(C1,F) :- relevantToFunc(C2,F), subconcern(C1,C2).


-isAssertion(P) :- property(P), not isAssertion(P).

% Identify the last step in the input
last_step(S) :-
	step(S),
	S2=S+1,
	not step(S2).

rule(R) :- input(R,"cpsf:addressesConcern",C).
addressesAtFunc(R,F) :- input(R,"cpsf:addressesAtFunc",F).
addressesConcern(R,C) :- input(R,"cpsf:addressesConcern",C).
addressesPolarity(R,P) :- input(R,"cpsf:addressesPolarity",PO), asp_polarity(PO,P).
%
hasCondition(R,C) :- input(R,"cpsf:hasCondition",C).
conditionProperty(C,A) :- input(C,"cpsf:conditionProperty",P), atomic_statement(P,A).
conditionPolarity(C,P) :- input(C,"cpsf:conditionPolarity",PO), asp_polarity(PO,P).
asp_polarity("cpsf:positive",pos).
asp_polarity("cpsf:negative",neg).


% ------ Theory ------

% transitive closure of subconcern/2
tc(subconcern(C1,C2)) :- subconcern(C1,C2).
tc(subconcern(C1,C2)) :- subconcern(C1,C3), tc(subconcern(C3,C2)).

% transitive closure of subconcern/2, reflexive variant
tc0(subconcern(C,C)) :- concern(C).
tc0(subconcern(C1,C2)) :- tc(subconcern(C1,C2)).


% ---------------> Impact of requirements on concerns <---------------
% ASSUMPTION: satisfaction of concerns does not affect satisfaction of properties
addresses(Q,C,F) :-
	rule(Rule),
	addressesAtFunc(Rule,F),
	addressesConcern(Rule,C),
	hasCondition(Rule,Cond),
	conditionProperty(Cond,Q).


holds(impacted(C,F,M),S) :-
	step(S),
	rule(Rule),
	addressesAtFunc(Rule,F),
	addressesConcern(Rule,C),
	addressesPolarity(Rule,M),
	body_satisfied(Rule,S).

body_satisfied(Rule,S) :-
	step(S),
	rule(Rule),
	not -body_satisfied(Rule,S).

-body_satisfied(Rule,S) :-
	step(S),
	rule(Rule),
	hasCondition(Rule,Cond),
% ASSUMPTION: satisfaction of concerns does not affect satisfaction of properties
	-condSat(Cond,S).

% ASSUMPTION: satisfaction of concerns does not affect satisfaction of properties
-condSat(Cond,S) :-
	step(S),
	hasCondition(Rule,Cond),
	conditionProperty(Cond,A),
	conditionPolarity(Cond,pos),
	not holds(sat(A),S).

% ASSUMPTION: satisfaction of concerns does not affect satisfaction of properties
-condSat(A,S) :-
	step(S),
	hasCondition(Rule,Cond),
	conditionProperty(Cond,A),
	conditionPolarity(Cond,neg),
	not -holds(sat(A),S).


% DEBUGGING
%condSat(Cond,S) :-
%	step(S),
%	hasCondition(Rule,Cond),
%	conditionProperty(Cond,A),
%	conditionPolarity(Cond,pos),
%	not -holds(sat(A),S).
%condSat(A,S) :-
%	step(S),
%	hasCondition(Rule,Cond),
%	conditionProperty(Cond,A),
%	conditionPolarity(Cond,neg),
%	not holds(sat(A),S).


% The satisfaction of requirements is handled explicitly
% by user-provided state constraints
%-holds(sat_property(A),S) :-
%	step(S),
%	atomic_statement(P,A),
%	isAssertion(P),
%	not holds(A,S).
%
%-holds(sat(C),S) :-
%	step(S),
%	addresses(C,P),
%	atomic_statement(P,A), 
%	-holds(sat_property(A),S).

fluent(sat(A)) :- atomic_statement(P,A).
fluent(sat(A)) :- config_feature(A).
fluent(sat(C,F)) :- relevantToFunc(C,F).
impact_mode(pos). impact_mode(neg).
fluent(impacted(C,F,M)) :- concern(C), isFunctionClass(F), impact_mode(M).


% sat_sub(C,F) holds iff every relevant sub-concern of C is satisfied
%-holds(sat_sub(C1,F),S) :-
%	step(S), relevantToFunc(C1,F),
%	subconcern(C1,C2), relevantToFunc(C2,F),
%	not holds(sat(C2,F),S).
%fluent(sat_sub(C,F)) :- relevantToFunc(C,F).
%defined(neg,sat_sub(C,F)) :- relevantToFunc(C,F).

% The satisfaction of C in F is impacted by some combination of requirements at S
impacted(C,F,S) :-
	step(S), relevantToFunc(C,F),impact_mode(M),
	holds(impacted(C,F,M),S).

% Concern C has at least one relevant sub-concern in function F
has_relevant_subconcern(C1,F) :-
	subconcern(C1,C2), relevantToFunc(C2,F).

% A concern is positively influenced if:
% 1. a combination of requirements impacts it positively OR
% 2. a relevant sub-concern is satisfied
positively_influenced(C,F,S) :-
	step(S), relevantToFunc(C,F),
	holds(impacted(C,F,pos),S).
positively_influenced(C1,F,S) :-
	step(S), relevantToFunc(C1,F),
%	has_relevant_subconcern(C1,F),
%	holds(sat_sub(C1,F),S).
	subconcern(C1,C2), relevantToFunc(C2,F),
	holds(sat(C2,F),S).

% A concern is negatively influenced if:
% 1. a combination of requirements impacts it negatively OR
% 2. a relevant sub-concern is unsatisfied
negatively_influenced(C,F,S) :-
	step(S), relevantToFunc(C,F),
	holds(impacted(C,F,neg),S).
negatively_influenced(C1,F,S) :-
	step(S), relevantToFunc(C1,F),
%	has_relevant_subconcern(C1,F),
%	-holds(sat_sub(C1,F),S).
	subconcern(C1,C2), relevantToFunc(C2,F),
	-holds(sat(C2,F),S).

% A concern is affected by uncertain influence (from its sub-concerns) if:
% 1. a relevant sub-concern has unknown satisfaction
uncertainly_influenced(C1,F,S) :-
	step(S), relevantToFunc(C1,F),
%	has_relevant_subconcern(C1,F),
%	not holds(sat_sub(C1,F),S),
%	not -holds(sat_sub(C1,F),S).
	subconcern(C1,C2), relevantToFunc(C2,F),
	not holds(sat(C2,F),S),
	not -holds(sat(C2,F),S).


%%%%%%%% INFERENCE ON CONCERN SATISFACTION
%
% Select the type of inference with:
%
%   inference(concerns,pessimistic)
%   inference(concerns,skeptical)
%   inference(concerns,optimistic)
%

% PESSIMISTIC INFERENCE ON CONCERN SATISFACTION
% This is the simplest case, where concerns default to unsatisfied
% 
% A concern (in a given function f, e.g. use case u1) is satisfied if:
%   1. it is positively influenced AND
%   2. it is not negatively influenced
holds(sat(C,F),S) :-
	inference(concerns,pessimistic),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S).

likelihood(sat(C,F),S,L) :-
	inference(concerns,pessimistic),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S),
	likelihood_sat(C,F,S,L).
	%degree_impacted_pos(C,F,S,L).

% A concern is unsatisfied in all other cases.
defined(pos,sat(C,F)) :- inference(concerns,pessimistic), relevantToFunc(C,F). 

% SKEPTICAL INFERENCE ON CONCERN SATISFACTION
% This is a more advanced case, where the satisfaction status of a
% concern may remain unknown/undecided/uncertain
% 
% A concern (in a given function f, e.g. use case u1) is satisfied if:
%   1. it is positively influenced AND
%   2. it is not negatively influenced AND
%   3. is not affected by uncertain influence
holds(sat(C,F),S) :-
	inference(concerns,skeptical),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S),
	not uncertainly_influenced(C,F,S).

likelihood(sat(C,F),S,D) :-
	inference(concerns,skeptical),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S),
	not uncertainly_influenced(C,F,S),
	likelihood_sat(C,F,S,D).
	%degree_impacted_pos(C,F,S,D).

% A concern is unsatisfied if:
%   1. it is negatively influenced AND
%   2. it is not positively influenced AND
%   3. is not affected by uncertain influence
-holds(sat(C,F),S) :-
	inference(concerns,skeptical),
	step(S), relevantToFunc(C,F),
	negatively_influenced(C,F,S),
	not positively_influenced(C,F,S),
	not uncertainly_influenced(C,F,S).
% OR
%   1. it has no relevant sub-concerns AND
%   2. it is not positively influenced AND
%   3. it is not negatively influenced
-holds(sat(C,F),S) :-
	inference(concerns,skeptical),
	step(S), relevantToFunc(C,F),
	not has_relevant_subconcern(C,F),
	not positively_influenced(C,F,S),
	not negatively_influenced(C,F,S).


% The satisfaction status of a concern is unknown in all other cases.
% Implemented by making sat(C,F) inertial rather than defined


% OPTIMISTIC INFERENCE ON CONCERN SATISFACTION
% This is another simple case, where concerns default to unsatisfied,
% but concerns that have no requirements nor sub-concerns are vacuously
% satisfied.
% 
% A concern (in a given function f, e.g. use case u1) is satisfied if:
%   1. it is positively influenced AND
%   2. it is not negatively influenced
holds(sat(C,F),S) :-
	inference(concerns,optimistic),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S).
likelihood(sat(C,F),S,D) :-
	inference(concerns,optimistic),
	step(S), relevantToFunc(C,F),
	positively_influenced(C,F,S),
	not negatively_influenced(C,F,S),
	likelihood_sat(C,F,S,D).
	%degree_impacted_pos(C,F,S,D).
% OR
%   1. it has no relevant sub-concerns AND
%   2. it is not positively influenced AND
%   3. it is not negatively influenced
holds(sat(C,F),S) :-
	inference(concerns,optimistic),
	step(S), relevantToFunc(C,F),
	not has_relevant_subconcern(C,F),
	not positively_influenced(C,F,S),
	not negatively_influenced(C,F,S).
likelihood(sat(C,F),S,D) :-
	inference(concerns,optimistic),
	step(S), relevantToFunc(C,F),
	not has_relevant_subconcern(C,F),
	not positively_influenced(C,F,S),
	not negatively_influenced(C,F,S),
	likelihood_sat(C,F,S,D).
	%degree_impacted_pos(C,F,S,D).

% A concern is unsatisfied in all other cases.
defined(pos,sat(C,F)) :- inference(concerns,optimistic), relevantToFunc(C,F). 


%%%% Relatedness of requirements across functions

% Definition. Requirement q1 is refined into requirement q2
% if they address the same concern in two functions F1 and F2
% and F1 is refined into F2.
refinedInto(Q1,Q2) :-
	addresses(Q1,C,F1),
	addresses(Q2,C,F2),
	refinedInto(F1,F2).

% Definition. Requirement q1 is related to requirement q2
% if there is a sequence r_1,...,r_k of requirements such that 
% q1 =r_1, q2=r_k, and every r_i is refined into r_i+1.
related(Q1,Q2) :-
	refinedInto(Q1,Q2),
	addresses(Q1,C,F1),	% make sure Q1, Q2 are requirements
	addresses(Q2,C,F2). % rather than functions

related(Q1,Q3) :-
	refinedInto(Q1,Q2),
	related(Q2,Q3).


%%%%%%%% OBSERVATIONS


% initial state of the CPS

holds(F,0) :-
	fluent(F),
	obs(F,true).

-holds(F,0) :-
	fluent(F),
	obs(F,false).

holds(F,0) :-
	fluent(F),
	assumed(F,true),
	not -holds(F,0).

-holds(F,0) :-
	fluent(F),
	assumed(F,false),
	not holds(F,0).

% Ad-hoc for prob_of_state functional fluent
holds(prob_of_state(100),0).

% next state: inertia axioms
is_defined(F) :- fluent(F), defined(M,F).

% NOTE: inertial for numerical fluents is defined on a case-by-case basis
-inertial(F) :- is_numerical(F).
-inertial(F) :- is_defined(F).

holds(F,S2) :-
	fluent(F),
	not -inertial(F),
	step(S), step(S2), S2=S+1,
	holds(F,S),
	not -holds(F,S2).

-holds(F,S2) :-
	fluent(F),
	not -inertial(F),
	step(S), step(S2), S2=S+1,
	-holds(F,S),
	not holds(F,S2).

holds(F,S) :-
	fluent(F),
	defined(neg,F),
	step(S),
	not -holds(F,S).

-holds(F,S) :-
	fluent(F),
	defined(pos,F),
	step(S),
	not holds(F,S).

% effect of a negative impact
-holds(A,S) :-
	impacted(neg,A,S).


% Ad-hoc treatment of prob_of_state functional fluent
holds(prob_of_state(P2),S2) :-
	step(S), step(S2), S2=S+1,
	holds(prob_of_state(P),S),
	do(A,S),
	prob_success(A,PSucc),
	P2a=P*PSucc,
	P2=P2a/100.

-unk_prob_success(S) :-
	step(S),
	do(A,S), prob_success(A,PSucc).
unk_prob_success(S) :-
	step(S),
	not -unk_prob_success(S).

holds(prob_of_state(P),S2) :-
	step(S), step(S2), S2=S+1,
	holds(prob_of_state(P),S),
	unk_prob_success(S).
