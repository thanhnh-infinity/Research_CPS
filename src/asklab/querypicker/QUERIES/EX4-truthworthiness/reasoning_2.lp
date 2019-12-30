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

% Step 7-1 : Middle layer: Representat bad tw if not exists
tw_bad_comp(Comp,0,S) :- not tw_bad_comp(Comp,_,S), component(Comp), step(S).

% Step 8: Compare and result

%% Case 1.1 : good higher, bad smaller
higher_TW(C1,C2,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good > TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad <= TW2_bad,
                       step(S).

%% Case 1.2.1 : good higher, bad higher, distance good > distance bad
higher_TW(C1,C2,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good > TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad > TW2_bad,
                       d_good = TW1_good - TW2_good,
                       d_bad = TW1_bad - TW2_bad,
                       d_good > d_bad,
                       step(S).

%% Case 1.2.2 : good higher, bad higher, distance good = distance bad
equal_TW(C1,C2,S)   :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good > TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad > TW2_bad,
                       d_good = TW1_good - TW2_good,
                       d_bad = TW1_bad - TW2_bad,
                       d_good = d_bad,
                       step(S).

%% Case 1.2.3 : good higher, bad higher, distance good > distance bad
higher_TW(C2,C1,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good > TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad > TW2_bad,
                       d_good = TW1_good - TW2_good,
                       d_bad = TW1_bad - TW2_bad,
                       d_good < d_bad,
                       step(S).

%% Case 2.1 : good equal, bad higher
higher_TW(C1,C2,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good = TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad < TW2_bad,
                       step(S).
%% Case 2.2 : good equal, bad higher
higher_TW(C2,C1,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good = TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad > TW2_bad,
                       step(S).
%% Case 2.2 : good equal, bad higher
equal_TW(C1,C2,S)  :- tw_good_comp(C1,TW1_good,S), 
                       tw_good_comp(C2,TW2_good,S), 
                       TW1_good = TW2_good,
                       tw_bad_comp(C1,TW1_bad,S),
                       tw_bad_comp(C2,TW2_bad,S),
                       TW1_bad = TW2_bad,
                       step(S).

equal_TW(C2,C1,S) :- equal_TW(C1,C2,S), component(C1), component(C2), step(S). 

% Step 9: Find the highest TW value

not_highest_TW(C2,S) :- component(C1),component(C2),
                        higher_TW(C1,C2,S), step(S).
highest_TW(C,S) :- component(C), not not_highest_TW(C,S), step(S).

% Action and changes

% ====== SHOW ========

#show tw_property/2.
%#show compGoodProp/3.
#show compBadProp/3.
#show tw_good_comp/3.
#show tw_bad_comp/3.
#show highest_TW/2.
%#show addrForConcern/2.
%#show order/3.

