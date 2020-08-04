#include "./ontology_LKAS_3_Positive.lp".
#include "./obs_init_state_LKAS.lp".

step(0).
%---- Reasoning Property Satisfaction by observation -----
h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).
h(P,0) :- property(P), not obs(P,false).

%---- Reasoning Concern Satisfaction by Minimal Formulas -----
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
% ---------------------------------------------

ref(X,P,C,T) :- h(in_mode(X,P),T), addressedBy(C,P), 
                component(X), property(P), concern(C), step(T).
pos(X,P,C,T) :- ref(X,P,C,T), possible_impacts_pos(X,P,C), h(sat(C),T).
neg(X,P,C,T) :- ref(X,P,C,T), not possible_impacts_pos(X,P,C).
neg(X,P,C,T) :- ref(X,P,C,T), not h(sat(C),T), concern(C), step(T).
pos(X,P,C,T) :- pos(X,P,C1,T), subconcern(C,C1), step(T).
neg(X,P,C,T) :- neg(X,P,C1,T), subconcern(C,C1), step(T).
twcp(X,TW,T) :- TW = #count{C,P:pos(X,P,C,T), property(P), concern(C)}, component(X), step(T).
twcn(X,TW,T) :- TW = #count{C,P:neg(X,P,C,T), property(P), concern(C)}, component(X), step(T).
d(X,D,T)     :- component(X), step(T), twcp(X,TWp,T), twcn(X,TWn,T), D=TWp-TWn.
most(X,T)    :- component(X), step(T), d(X,M,T), M == #max{N:d(_,N,T)}.
least(X,T)   :- component(X), step(T), d(X,M,T), M == #min{N:d(_,N,T)}.

%#show h/2.%
%#show ref/4.
%#show pos/4.
%#show neg/4.
#show twcp/3.
#show twcn/3.
#show most/2.
#show least/2.