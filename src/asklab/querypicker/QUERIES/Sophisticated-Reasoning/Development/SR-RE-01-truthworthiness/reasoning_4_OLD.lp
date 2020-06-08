%%%%%%%
% Satisfaction Theory + Positive Impacts Degree
%%%%%%%

step(0).

%-------The Ontology---------------------
% concern 
aspect(trustworthiness).

concern(all).
concern(trustworthiness).
concern(safety).
concern(reliability).
concern(security).
concern(resilience).
concern(privacy).

concern(functional_safety).
concern(cyber_security).
concern(physical_security).
concern(predictability).
concern(manageability).
concern(dissociability).

concern(severity).
concern(controllability).
concern(frequency).
concern(confidentiality).
concern(integrity).
concern(availability).
concern(controls).
concern(transparency).
concern(innovation).
concern(ultility).

concern(encryption).
concern(verification).
concern(authorization).
concern(authentication).

% subconcern relation
subconcern(all,trustworthiness).

subconcern(trustworthiness,safety).
subconcern(trustworthiness,reliability).
subconcern(trustworthiness,security).
subconcern(trustworthiness,resilience).
subconcern(trustworthiness,privacy).

subconcern(safety,functional_safety).

subconcern(security,cyber_security).
subconcern(security,physical_security).

subconcern(privacy,predictability).
subconcern(privacy,manageability).
subconcern(privacy,dissociability).

subconcern(functional_safety,severity).
subconcern(functional_safety,frequency).
subconcern(functional_safety,controllability).

subconcern(cyber_security,confidentiality).
subconcern(cyber_security,integrity).
subconcern(cyber_security,availability).

subconcern(physical_security,ultility).

subconcern(predictability,controls).
subconcern(predictability,transparency).
subconcern(predictability,innovation).

subconcern(confidentiality,encryption).
subconcern(confidentiality,verification).


subconcern(controls,authorization).
subconcern(controls,authentication).

% Property

property(data_encrypted).
property(conn_encrypted).
property(protocol_encrypted).

property(algo_AES).
property(algo_RSA).
property(algo_DES).

property(firewall_setup).
property(ip_filtering).
property(mac_check).

property(secure_boot).

property(energy_mode).
property(operation_mode).

property(trusted_auth_device).
property(trusted_environment).
property(auth_strategies).

% Addressed : Relation Properties-Concerns
addressedBy(encryption,data_encrypted).
addressedBy(encryption,conn_encrypted).
addressedBy(encryption,protocol_encrypted).
addressedBy(encryption,algo_AES).
addressedBy(encryption,algo_RSA).
addressedBy(encryption,algo_DES).

addressedBy(verification,firewall_setup).
addressedBy(verification,ip_filtering).
addressedBy(verification,mac_check).

addressedBy(integrity,secure_boot).
addressedBy(integrity,energy_mode).
addressedBy(integrity,operation_mode).

addressedBy(authorization,trusted_auth_device).
addressedBy(authorization,trusted_environment).
addressedBy(authorization,auth_strategies).


% Observe Property
obs(data_encrypted,true).
obs(conn_encrypted,true).
obs(protocol_encrypted,true).
obs(algo_AES,true).
obs(algo_RSA,true).
obs(algo_DES,true).

obs(firewall_setup,true).
obs(ip_filtering,true).

obs(trusted_auth_device,true).
obs(trusted_environment,true).
obs(auth_strategies,unknown).

obs(secure_boot,true).
obs(energy_mode,unknown).
obs(operation_mode,unknown).


% Property Requirement
group(1..5).
%--- For Auth_Strategies
requirement(finger_printing).
requirement(two_factors).
requirement(iris_scan).
requirement(oauth).
requirement(opt_code).
requirement(email_verify).
requirement(ip_check).

obs(finger_printing,true).
obs(two_factors,true).
obs(iris_scan,false).
obs(oauth,false).
obs(opt_code,true).
obs(email_verify,true).
obs(ip_check,true).

suppBy(finger_printing,auth_strategies,1).
suppBy(two_factors,auth_strategies,2).
suppBy(iris_scan,auth_strategies,3).
suppBy(oauth,auth_strategies,4).
suppBy(opt_code,auth_strategies,4).
suppBy(oauth,auth_strategies,5).
suppBy(email_verify,auth_strategies,5).
suppBy(ip_check,auth_strategies,5).

%--- For Operation_Mode
requirement(advanced_mode).
requirement(basic_mode).

obs(advanced_mode,true).
obs(basic_mode,true).

suppBy(advanced_mode,operation_mode,1).
suppBy(basic_mode,operation_mode,2).

%--- For Energy_Mode
requirement(saving_mode).
requirement(powerful_mode).
requirement(normal_mode).

obs(saving_mode,true).
obs(powerful_mode,true).
obs(normal_mode,true).

suppBy(saving_mode,energy_mode,1).
suppBy(powerful_mode,energy_mode,2).
suppBy(normal_mode,energy_mode,3).

% Component
%---- Define component ----
component(sam).
component(cam).
component(battery).

%---- Define Possible Positive Relation of each component
possible_rel_pos(sam,data_encrypted).
possible_rel_pos(sam,conn_encrypted).
possible_rel_pos(sam,algo_RSA).
possible_rel_pos(sam,algo_AES).
possible_rel_pos(sam,firewall_setup).
possible_rel_pos(sam,mac_check).
possible_rel_pos(sam,secure_boot).
possible_rel_pos(sam,advanced_mode).
possible_rel_pos(sam,iris_scan).
possible_rel_pos(sam,two_factors).
possible_rel_pos(sam,finger_printing).


possible_rel_pos(cam,data_encrypted).
possible_rel_pos(cam,conn_encrypted).
possible_rel_pos(cam,protocol_encrypted).
possible_rel_pos(cam,mac_check).
possible_rel_pos(cam,secure_boot).
possible_rel_pos(cam,advanced_mode).
possible_rel_pos(cam,trusted_auth_device).

possible_rel_pos(battery,powerful_mode).

%---- Current Action Relation to property----
relation(sam,data_encrypted).
relation(sam,algo_RSA).
relation(sam,firewall_setup).
relation(sam,secure_boot).

relation(cam,ip_filtering).
relation(cam,data_encrypted).
relation(cam,conn_encrypted).
relation(cam,secure_boot).
relation(cam,trusted_auth_device).

%---- Current Action Relation to property requirement ----
relation(sam,advanced_mode).
relation(sam,finger_printing).
relation(cam,advanced_mode).
relation(battery,saving_mode).

%--- Reasoning first step
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

