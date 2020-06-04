#include "./ontology_LKAS.lp".
#include "./obs_init_state_LKAS_4.lp".

%==============================================
step(0).

%%%%%%%
% Satisfaction Theory + Positive Impacts Degree
%%%%%%%

%--- Reasoning first step -----------
h(use(C,P),0) :- property(P), component(C), step(0), active(C,P).

%---- Reasoning Property Satisfaction by observation -----
h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).
h(P,0) :- property(P), not obs(P,false).

%---- Reasoning Concern Satisfaction by Formulae of properties -----
-sat_formulas(C,F,G,T) :- concern(C), property(P), formulas(G), 
                          func_dec(F,C), addressedBy(C,P), member(P,G), addressToFunc(C,F,G),
                          not h(P,T), step(T).
sat_formulas(C,F,G,T) :- concern(C), formulas(G), func_dec(F,C), addressToFunc(C,F,G),
                         not -sat_formulas(C,F,G,T), step(T).
-h(sat(C,F),T) :- concern(C), func_dec(F,C), step(T), not sat_formulas(C,F,_,T).
h(sat(C,F),T)  :- not -h(sat(C,F),T), step(T), func_dec(F,C).
-h(sat(C),T)   :- concern(C), func_dec(F,C), not h(sat(C,F),T), step(T).
-h(sat(C),T)   :- concern(C), func_dec(F,C), -h(sat(C,F),T), step(T).

%---- Traditiona Reasoning about Concern Satisfaction ---                       
-h(sat(C),T) :- -h(P,T), property(P), step(T),  addressedBy(C,P), 
                 not member(P,_).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T) :- not -h(sat(C),T), concern(C), step(T).

%=============================
#show -h/2.