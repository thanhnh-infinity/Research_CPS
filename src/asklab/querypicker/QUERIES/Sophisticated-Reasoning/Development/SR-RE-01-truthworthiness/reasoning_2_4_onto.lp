#include "./CPS_Ontology.lp".
#include "./ontology_driven.lp".
#include "./ontology_init.lp".

%#include "./ontology_LKAS_2.lp".
%#include "./obs_init_state_LKAS.lp".
%=================================
#const n = 2.
step(0..n).
%=====Satisfaction Reasoning======
%h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false).
%h(P,0) :- obs(availablePatch(P),true), property(P).
h(P,0) :- obs(P,true).
h(P,0) :- property(P), not obs(P,false).

-h(sat(C),T) :- -h(P,T), property(P), step(T), 
                addressedBy(C,P).
-h(sat(X),T) :- concern(X), concern(Y), 
                subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T) :- concern(X), concern(Y), 
                subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T) :- not -h(sat(C),T), concern(C), step(T).

-h(sat(all),T)  :- 1{-h(sat(A),T); not h(sat(A),T)},
                   aspect(A), step(T).
h(sat(all),T)   :- not -h(sat(all),T), step(T).
% ---------------------------------------------
% ==========  ACTIONS and CHANGES =============
% ---------------------------------------------
% Generate action
1{occurs(A,T):action(A)}1 :- step(T), T<n.
:- occurs(A,T), not executable(A,T).

% Inertial axioms
fluent(F) :- property(F).
fluent(availablePatch(F)) :- property(F).
%fluent(sat(A)) :- concern(A).

h(F,T+1)    :- h(F,T), not -h(F,T+1), step(T), fluent(F).
-h(F,T+1)   :- -h(F,T), not h(F,T+1), step(T), fluent(F).

% Goal check type 2
%goal(G) :- h(sat(trustworthiness),G), step(G).
%success :- goal(G), G <= n, step(G).
%:- not success.

% Goal check type 1
:- not h(sat(C),n), concern(C).
%:- not h(sat(A),n), aspect(A).

% Actions
action(tOn(X)) :- property(X).
action(patch(X)) :- property(X).

%% Preconditions
%executable(tOn(detect_No_passenger),T) :- -h(detect_No_passenger,T), step(T).
%executable(tOn(control_speed),T) :- -h(control_speed,T), step(T).
%executable(patch(control_speed),T) :- -h(control_speed,T), step(T).

executable(tOn(X),T) :- -h(X,T), property(X), step(T).
executable(patch(X),T) :- -h(X,T), h(availablePatch(X),T), property(X), step(T).

%% Effects
h(X,T+1) :- occurs(tOn(X),T), step(T).
h(X,T+1) :- occurs(patch(X),T), step(T).

%:- occurs(A1,T), occurs(A2,T), A1 != A2.

% ---------------------------------------------
% ==========  Probabilistic of success ========
% ---------------------------------------------
prob_success(tOn(detect_No_passenger),80).
prob_success(tOn(control_speed),70).
prob_success(patch(control_speed),30).

prob_success(tOn("cpsf:Firewall_Setup"),60).
prob_success(tOn("cpsf:Two_Factors"),70).
prob_success(patch("cpsf:Two_Factors"),30).
prob_success(patch("cpsf:Firewall_Setup"),20).

% ---------------------------------------------

h(prob_of_state(100),0).
h(prob_of_state(P2),T2) :- step(T),step(T2), T2=T+1, 
                           h(prob_of_state(P),T), 
                           occurs(A,T), 
                           prob_success(A,PSucc),
                           P2a=P*PSucc,P2=P2a/100.
known_prob_success(T)   :- step(T), occurs(A,T), 
                           prob_success(A,PSucc).
unknown_prob_success(T) :- step(T), not known_prob_success(T).
h(prob_of_state(P),T2)  :- step(T), step(T2), T2=T+1, 
                           h(prob_of_state(P),T), 
                           unknown_prob_success(T).
last_step(T):- step(T),T2=T+1, not step(T2).
check_p(P,T) :- h(prob_of_state(P),T).
%last_step(1). 
#maximize{P : h(prob_of_state(P),T), last_step(T)}.

% ---------------------------------------------
#show occurs/2.
%#show executable/2.
#show check_p/2.
%#show action/1.
%#show h/2.