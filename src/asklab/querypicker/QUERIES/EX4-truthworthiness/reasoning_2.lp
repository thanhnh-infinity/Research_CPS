%=====REASONING TRUTHWORTHINESS with STEP======

% =====Configuration=========
%sol(addr).
sol(all).

% =====State of CPS System===
step(0).

% =====Ontology============== (Step 1)
relevantToFunc(a1,f).
relevantToFunc(b1,f).
relevantToFunc(b0,f).
relevantToFunc(c1,f).
relevantToFunc(c2,f).

% Order sibling concerns
%order(SC,F,N):-
%    subconcern(C,SC), relevantToFunc(SC,F),
%    N = { SC < SCp : subconcern(C,SCp), relevantToFunc(SCp,F) }.

subconcern(b1,a1).
subconcern(b0,b1).
%subconcern(b0,c1).
%subconcern(b1,c1).
%subconcern(b1,c2).

addressedBy(a1,x).
addressedBy(a2,x).
addressedBy(a3,x).
addressedBy(a3,y).
addressedBy(b1,y).
addressedBy(b1,z).
addressedBy(b2,z).
addressedBy(b3,z).
addressedBy(a2,z).
addressedBy(b1,t).
addressedBy(b2,t).
addressedBy(b3,t).
addressedBy(a2,t).

property(x).
property(y).
property(z).
property(t).


% ======Physical CPS System (step 3)
component(c1).
component(c2).
component(c3).
relation(c1,x).
relation(c1,y).
relation(c2,y).
relation(c2,x).
relation(c2,z).
relation(c3,z).
relation(c3,t).

% ======Observation for Initial State
obs(x,true).
obs(y,true).
obs(z,true).
obs(t,true).

%----------------------------------------------
%=====REASONING TRUTHWORTHINESS with STEP======
%----------------------------------------------

% Step 2 : Representation the property P in initial state of CPS 
holds(P,0) :- obs(P,true), property(P).
-holds(P,0) :- obs(P,false), property(P).

% Step 3: Check addresses links
addrForConcern(P,C) :- property(P), 
					   addressedBy(C,P), 
					   sol(all).
addrForConcern(P,C) :- addrForConcern(P,C1), 
                       subconcern(C,C1), 
                       sol(all).
                       
% Step 4 [1,2]: Reasoning a component C has good/bad property P at step S.
compGoodProp(Com,P,S) :- relation(Com,P), holds(P,S), 
						 component(Com), property(P), step(S).
compBadProp(Com,P,S)  :- component(Com), property(P), step(S),
                         relation(Com,P), -holds(P,S).

% Step 5: Compute the tw_property: total number of links to the concerns that are addressed by and related to property P
tw_property(P,N) :- N=#count{C : addressedBy(C,P)}, 
                        property(P), sol(addr).
tw_property(P,N) :- N=#count{C : addrForConcern(P,C)}, 
                        property(P), sol(all).

% Step 6: Compute the good trustworthiness value of component C
tw_good_comp(Comp,TWvalue,S) :- component(Comp), step(S),
								TWvalue= #sum{N,P : tw_property(P,N), property(P), compGoodProp(Comp,P,S)}.

% Step 7: Compute the bad trustworthiness value of component C
tw_bad_comp(Comp,TWvalue,S) :- component(Comp), step(S),
                               TWvalue= #sum{N,P : tw_property(P,N), property(P), compBadProp(Comp,P,S)}.

% Step 8: Compare and result

higher_TW(C1,C2,S) :- tw_good_comp(C1,TW1,S), 
                      tw_good_comp(C2,TW2,S), 
                      TW1 > TW2, step(S).
not_highest_TW(C2,S) :- component(C1),component(C2),
                        higher_TW(C1,C2,S), step(S).
highest_TW(C,S) :- component(C), not not_highest_TW(C,S), step(S).

% Action and changes

% ====== SHOW ========

#show tw_property/2.
%#show compGoodProp/3.
#show compBadProp/3.
#show tw_good_comp/3.
#show highest_TW/2.
%#show addrForConcern/2.
%#show order/3.

