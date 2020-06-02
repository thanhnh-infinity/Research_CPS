#include "./ontology_LKAS_1.lp".

%%%%%%%
% Satisfaction Theory + Positive Impacts Degree
%%%%%%%

step(0).

%--- Reasoning first step -----------
h(use(C,P),0) :- property(P), component(C), step(T), relation(C,P).
h(use(C,R),0) :- requirement(R), component(C), step(T), relation(C,R).

%---- Traditiona Reasoning about Property and Concern Satisfaction ---
h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).

-h(sat(C),T) :- -h(P,T), property(P), step(T), addressedBy(C,P), step(T).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T) :- not -h(sat(C),T), concern(C), step(T).

%---- Reasoning Property Satisfaction by Property Requirements -----
%leadTo(P,G) :- property(P), obs(P,unknown), group(G), N = #count{R : suppBy(R,P,G), obs(R,true)}, M = #count{R : suppBy(R,P,G)}, M = N, M > 0.

leadTo(P,G) :- property(P), obs(P,unknown), group(G), N = #count{R : suppBy(R,P,G), not obs(R,true)}, M = #count{R : suppBy(R,P,G)}, M > 0, N = 0. 

h(P,0) :- leadTo(P,G), property(P), group(G).
-h(P,0) :- not h(P,0), property(P).

%---- Reasoning Property Satisfaction by Property Requirements ----

%%%%% --- Default Assignment PID values for Property Requirements --
%deg_req(advanced_mode,operation_mode,8,0).
%deg_req(basic_mode,operation_mode,6,0).
%deg_req(saving_mode,energy_mode,2,0).
%deg_req(normal_mode,energy_mode,7,0).
%deg_req(powerful_mode,energy_mode,9,0).
%deg_req(finger_printing,auth_strategies,7,0).
%deg_req(two_factors,auth_strategies,6,0).
%deg_req(oauth,auth_strategies,5,0).
%deg_req(opt_code,auth_strategies,3,0).
%deg_req(email_verify,auth_strategies,3,0).
%deg_req(ip_check,auth_strategies,3,0).

%%%%% --- Default Assignment PID values for Property NOT have any supports --
%deg_prop(secure_boot,integrity,6,0).
%deg_prop(firewall_setup,verification,7,0).
%deg_prop(ip_filtering,verification,3,0).
%deg_prop(algo_RSA,encryption,8,0).
%deg_prop(algo_AES,encryption,6,0).
%deg_prop(protocol_encrypted,encryption,10,0).
%deg_prop(data_encrypted,encryption,10,0).

%%%%%
%order_requirement(R,P,N)  :- suppBy(R,P,_), 
%                               N = { R < Rp : suppBy(Rp,P,_)}.
%has_requirement(P)        :- suppBy(R,P,_), property(P), requirement(R).
%-has_requirement(P)       :- property(P), not has_requirement(P).

%deg_prop_imp_sub(P,1,T)   :- step(T), property(P), -has_requirement(P). 
%deg_prop_imp(P,N,T)       :- step(T), property(P), 
%                             deg_prop_imp_sub(P,N1,T), 
%                             deg_prop(P,_,N2,T), N=N1*N2.
%deg_prop_imp_req_aux(P,0,X,T) :- step(T), suppBy(R,P,_), order_requirement(R,P,0),                              
%                                 deg_req(R,P,X,T), h(use(Com,R),T), component(Com).
%deg_prop_imp_req_aux(P,0,1,T) :- step(T), suppBy(R,P,_), order_requirement(R,P,0),                              
%                                 deg_req(R,P,X,T), not h(use(Com,R),T), component(Com).
%likelihood_sat_sub_aux(P,N,V,T) :- step(T), subconcern(C,SC), order(SC,C,N), 
%                                   likelihood_sat(SC,Y,T), likelihood_sat_sub_aux(C,N-1,X,T), 
%                                   V=X*Y. 
%likelihood_sat_sub(C,X,T)       :- step(T), concern(C), 
%                                   likelihood_sat_sub_aux(C,N,X,T), 
%                                   not likelihood_sat_sub_aux(C,N+1,_,T).
%------------------------------------------------------------------
%---- Reasoning Positive Impacts Degree ---------------
%degree_pos(encryption,80,0).
%degree_pos(verification,21,0).
%degree_pos(integrity,12,0).
%degree_pos(authorization,70,0).
%degree_pos(C,1,T) :- concern(C), N=#count{P : addressedBy(C,P),property(P)}, 
%                     N<=0, step(T).


no_all_pos_concern(C,N1+N2,T) :- concern(C), step(T), 
                                 N1=#count{R,Com : component(Com),
                                           requirement(R),property(P),
                                           possible_rel_pos(Com,R),
                                           addressedBy(C,P), suppBy(R,P,_)}, 
                                 N2=#count{P,Com : component(Com),property(P),
                                           possible_rel_pos(Com,P),
                                           addressedBy(C,P)}.

no_act_pos_concern(C,N1+N2,T) :- concern(C), step(T), 
                                 N1=#count{R,Com : component(Com),
                                           requirement(R),property(P),
                                           possible_rel_pos(Com,R),
                                           addressedBy(C,P), 
                                           suppBy(R,P,_), h(use(Com,R),T)
                                           }, 
                                 N2=#count{P,Com : component(Com),property(P),
                                           possible_rel_pos(Com,P),
                                           addressedBy(C,P), h(use(Com,P),T)}.

degree_pos(C,1,T) :- step(T), concern(C), no_all_pos_concern(C,0,T).
degree_pos(C,N1*100/N2,T) :- concern(C), no_act_pos_concern(C,N1,T), no_all_pos_concern(C,N2,T), N2!=0.

%--- Reasoning Algorithm Likelihood of Concern Satisfaction ----
order(SC,C,N)      :- subconcern(C,SC), N = { SC < SCp : subconcern(C,SCp)}.
has_subconcern(C)  :- subconcern(C,SC), concern(C), concern(SC).
-has_subconcern(C) :- concern(C), not has_subconcern(C).

likelihood_sat_sub(C,1,T)       :- step(T), concern(C), -has_subconcern(C). 
likelihood_sat(C,N,T)           :- step(T), concern(C), 
                                   likelihood_sat_sub(C,N1,T), 
                                   degree_pos(C,N2,T), N=N1*N2.
likelihood_sat_sub_aux(C,0,X,T) :- step(T), subconcern(C,SC), order(SC,C,0), 
                                   likelihood_sat(SC,X,T).
likelihood_sat_sub_aux(C,N,V,T) :- step(T), subconcern(C,SC), order(SC,C,N), 
                                   likelihood_sat(SC,Y,T), likelihood_sat_sub_aux(C,N-1,X,T), 
                                   V=X*Y. 
likelihood_sat_sub(C,X,T)       :- step(T), concern(C), 
                                   likelihood_sat_sub_aux(C,N,X,T), 
                                   not likelihood_sat_sub_aux(C,N+1,_,T).
%------------------------------------------------------------------
%#show h/2.
%#show -h/2.
%#show leadTo/2.
%#show deg/4.
%#show order/3.
#show likelihood_sat/3.
%#show likelihood_sat_sub_aux/4.
%#show degree_pos/3.
%#show deg_prop_sat/3.
%#show order_requirement/3.
%#show deg_prop_imp_req_aux/4.
%#show no_act_pos_concern/3.
%#show degree_pos_temp/3.

