#include "./ontology_elevator.lp".
#include "./obs_init_state_elevator.lp".

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

%=========================================
#show occurs/2.
%#show executable/2.
%#show check_p/2.
%#show action/1.
%#show h/2.