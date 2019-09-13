%
% Calculation of degree of satisfaction of positively-impacting requirements.
% Requires clingo. Not supported by dlv.
%

degree_impacted_pos(C,F,S,N) :-
	step(S), relevantToFunc(C,F),
	N1=#count{ Rule: rule(Rule),
		  addressesAtFunc(Rule,F),
		  addressesConcern(Rule,C),
		  addressesPolarity(Rule,pos),
		  body_satisfied(Rule,S)
		},
	N2=#count{ Rule: rule(Rule),
		  addressesAtFunc(Rule,F),
		  addressesConcern(Rule,C),
		  addressesPolarity(Rule,pos)
		},
	N2!=0,
	N=N1*100/N2.

degree_impacted_pos(C,F,S,100) :-
	step(S), relevantToFunc(C,F),
	N2=#count{ Rule: rule(Rule),
		  addressesAtFunc(Rule,F),
		  addressesConcern(Rule,C),
		  addressesPolarity(Rule,pos)
		},
	N2=0.


% Order sibling concerns
order(SC,F,N):-
	subconcern(C,SC), relevantToFunc(SC,F),
	N = { SC < SCp : subconcern(C,SCp), relevantToFunc(SCp,F) }.

likelihood_sat_sub_aux(C,F,0,S,X) :- step(S), relevantToFunc(C,F), subconcern(C,SC),order(SC,F,0),likelihood_sat(SC,F,S,X).
likelihood_sat_sub_aux(C,F,N,S,X*Y/100) :- step(S), relevantToFunc(C,F), subconcern(C,SC),order(SC,F,N),likelihood_sat(SC,F,S,Y),likelihood_sat_sub_aux(C,F,N-1,S,X).
has_subconcerns(C) :- subconcern(C,SC).
-has_subconcerns(C) :- concern(C), not has_subconcerns(C).
likelihood_sat_sub(C,F,S,100) :- step(S), concern(C),  relevantToFunc(C,F), -has_subconcerns(C).
likelihood_sat_sub(C,F,S,X) :- step(S), concern(C),  relevantToFunc(C,F), likelihood_sat_sub_aux(C,F,N,S,X),not likelihood_sat_sub_aux(C,F,N+1,S,_).

likelihood_sat(C,F,S,N) :- step(S), concern(C), relevantToFunc(C,F), likelihood_sat_sub(C,F,S,N1),degree_impacted_pos(C,F,S,N2),N=N1*N2/100.
