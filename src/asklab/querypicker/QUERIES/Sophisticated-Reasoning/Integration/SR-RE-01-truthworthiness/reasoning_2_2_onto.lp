%=================================
step(0).
%=====Satisfaction Reasoning======
h(P,0)  :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).
h(P,0)  :- property(P), not obs(P,false).

-h(sat(C),T)   :- -h(P,T), property(P), step(T), 
                  addressedBy(C,P).
-h(sat(X),T)   :- concern(X), concern(Y), 
                  subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T)   :- concern(X), concern(Y), 
                  subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T)    :- not -h(sat(C),T), concern(C), step(T).

%-h(sat(all),T) :- 1{-h(sat(trustworthiness),T); not h(sat(trustworthiness),T)}, step(T).
-h(sat(all),T) :- -h(sat(A),T), aspect(A), step(T).
h(sat(all),T)  :- not -h(sat(all),T), step(T).
% ---------------------------------------------

