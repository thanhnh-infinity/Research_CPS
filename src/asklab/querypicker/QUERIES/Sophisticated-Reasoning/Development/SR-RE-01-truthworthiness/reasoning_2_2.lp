#include "./ontology_elevator.lp".
#include "./obs_init_state_elevator.lp".

%#include "./ontology_LKAS_2.lp".
%#include "./obs_init_state_LKAS.lp".

step(0).
%=====Satisfaction Reasoning======

h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).

-h(sat(C),T) :- -h(P,T), property(P), step(T), 
                addressedBy(C,P).
-h(sat(X),T) :- concern(X), concern(Y), 
                subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T) :- concern(X), concern(Y), 
                subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T) :- not -h(sat(C),T), concern(C), step(T).

-h(sat(all),T) :- 1{-h(sat(trustworthiness),T); not h(sat(trustworthiness),T)}, step(T).
h(sat(all),T) :- not -h(sat(all),T), step(T).
% ---------------------------------------------
#show -h/2.

