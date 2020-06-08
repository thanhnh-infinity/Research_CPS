#include "./ontology_elevator.lp".
#include "./obs_init_state_elevator.lp".

%#include "./ontology_LKAS_2.lp".
%#include "./obs_init_state_LKAS.lp".

%=====REASONING TRUTHWORTHINESS with STEP======

% =====Configuration=========
%sol(addr).
sol(all).

% =====State of CPS System===
step(0).

%----------------------------------------------
%=====REASONING TRUTHWORTHINESS with STEP======
%----------------------------------------------

% -- Step 2 : Representation the property P in initial state of CPS 
holds(P,0) :- obs(P,true), property(P).
-holds(P,0) :- obs(P,false), property(P).

% -- Step 3: Check addresses links
addrForConcern(P,C) :- property(P), 
					             addressedBy(C,P), 
					             sol(all).
addrForConcern(P,C) :- addrForConcern(P,C1), 
                       subconcern(C,C1), 
                       sol(all).
                       
% -- Step 4 [1,2]: Reasoning a component C has good/bad property P at step S.
compGoodProp(Com,P,S) :- relation(Com,P), holds(P,S), 
						             component(Com), property(P), step(S).
compBadProp(Com,P,S)  :- component(Com), property(P), step(S),
                         relation(Com,P), -holds(P,S).

% -- Step 5: Compute the tw_property: total number of links to the concerns that are addressed by and related to property P
tw_property(P,N) :- N=#count{C : addressedBy(C,P)}, 
                    property(P), sol(addr).
tw_property(P,N) :- N=#count{C : addrForConcern(P,C)}, 
                    property(P), sol(all).

% -- Step 6: Compute the good trustworthiness value of component C
tw_good_comp(Comp,TWvalue,S) :- component(Comp), step(S),
								                TWvalue = #sum{N,P : tw_property(P,N), property(P), compGoodProp(Comp,P,S)}.

% -- Step 7: Compute the bad trustworthiness value of component C
tw_bad_comp(Comp,TWvalue,S)  :- component(Comp), step(S),
                                TWvalue = #sum{N,P : tw_property(P,N), property(P), compBadProp(Comp,P,S)}.

% -- Step 7-1 : Middle layer: Representation good/bad tw if not exists
tw_good_comp(Comp,0,S)  :- not tw_good_comp(Comp,_,S), 
                           component(Comp), step(S).
tw_bad_comp(Comp,0,S)   :- not tw_bad_comp(Comp,_,S), 
                           component(Comp), step(S).

% -- Step 8: Ordering and result
distance(C,D,S) :- component(C), step(S), tw_good_comp(C,TWp,S),
                   tw_bad_comp(C,TWn,S), D = TWp-TWn. 

% -- Step 9: Find the highest/lowest TW value
highest_TW_comp(C,S) :- component(C), step(S), distance(C,M,S),
                        M == #max{N:distance(_,N,S)}.
lowest_TW_comp(C,S)  :- component(C), step(S), distance(C,M,S),
                        M == #min{N:distance(_,N,S)}.
%----------------------------------------------


% ====== SHOW ========
#show tw_property/2.
%#show compGoodProp/3.
%#show compBadProp/3.
#show tw_good_comp/3.
#show tw_bad_comp/3.
#show highest_TW_comp/2.
#show lowest_TW_comp/2.
%#show addrForConcern/2.
%#show addressedBy/2.
%#show order/3.
#show distance/3.

