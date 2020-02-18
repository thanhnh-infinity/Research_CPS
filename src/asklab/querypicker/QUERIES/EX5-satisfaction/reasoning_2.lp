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


property(finger_printing).
property(two_factors).
property(iris_scan).
property(oauth).
property(opt_code).
property(email_verify).
property(ip_check).

property(trusted_auth_device).
property(trusted_environment).

property(advanced_mode).
property(basic_mode).

property(saving_mode).
property(powerful_mode).
property(normal_mode).



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
addressedBy(integrity,advanced_mode).
addressedBy(integrity,basic_mode).

addressedBy(integrity,saving_mode).
addressedBy(integrity,powerful_mode).
addressedBy(integrity,normal_mode).



addressedBy(authorization,finger_printing).
addressedBy(authorization,two_factors).
addressedBy(authorization,iris_scan).
addressedBy(authorization,oauth).
addressedBy(authorization,opt_code).
addressedBy(authorization,email_verify).
addressedBy(authorization,ip_check).

addressedBy(authorization,trusted_auth_device).
addressedBy(authorization,trusted_environment).




% Observe Property
obs(data_encrypted,true).
obs(conn_encrypted,true).
obs(protocol_encrypted,true).
obs(algo_AES,true).
obs(algo_RSA,true).
obs(algo_DES,true).

obs(firewall_setup,true).
obs(ip_filtering,true).


obs(secure_boot,true).


obs(trusted_auth_device,true).
obs(trusted_environment,true).

obs(finger_printing,true).
obs(two_factors,false).
obs(iris_scan,true).
obs(oauth,false).
obs(opt_code,true).
obs(email_verify,false).
obs(ip_check,true).

obs(advanced_mode,true).
obs(basic_mode,true).

obs(saving_mode,true).
obs(powerful_mode,true).
obs(normal_mode,true).

% Formulas
formulas(1..5).

func_dec(sign_in_func,authorization).
func_dec(operation_func,integrity).
func_dec(energy_func,integrity).

addressToFunc(finger_printing,authorization,sign_in_func,1).
addressToFunc(two_factors,authorization,sign_in_func,2).
addressToFunc(iris_scan,authorization,sign_in_func,3).
addressToFunc(oauth,authorization,sign_in_func,4).
addressToFunc(opt_code,authorization,sign_in_func,4).
addressToFunc(oauth,authorization,sign_in_func,5).
addressToFunc(email_verify,authorization,sign_in_func,5).
addressToFunc(ip_check,authorization,sign_in_func,5).

%--- For Operation_Mode
addressToFunc(advanced_mode,integrity,operation_func,1).
addressToFunc(basic_mode,integrity,operation_func,2).

%--- For Energy_Mode
addressToFunc(saving_mode,integrity,energy_func,1).
addressToFunc(powerful_mode,integrity,energy_func,2).
addressToFunc(normal_mode,integrity,energy_func,3).

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

%%%%%%%
% Satisfaction Theory + Positive Impacts Degree
%%%%%%%

step(0).

%--- Reasoning first step -----------
h(use(C,P),0) :- property(P), component(C), step(T), relation(C,P).

%---- Reasoning Property Satisfaction by observation -----
h(P,0) :- obs(P,true), property(P).
-h(P,0) :- obs(P,false), property(P).

%---- Reasoning Concern Satisfaction by Minimal Formulas -----
sat_formulas(C,F,G,T):- concern(C), formulas(G), func_dec(F,C), step(T), 
                        N=#count{P : addressToFunc(P,C,F,G), not h(P,T)},
                        N=0, M=#count{P : addressToFunc(P,C,F,G)}, M>0.

-h(sat(C,F),T) :- concern(C), func_dec(F,C), step(T), not sat_formulas(C,F,_,T).
h(sat(C,F),T)  :- not -h(sat(C,F),T), step(T), func_dec(F,C).
-h(sat(C),T)   :- concern(C), func_dec(F,C), not h(sat(C,F),T), step(T).
-h(sat(C),T)   :- concern(C), func_dec(F,C), -h(sat(C,F),T), step(T).


%---- Traditiona Reasoning about Concern Satisfaction ---
-h(sat(C),T) :- -h(P,T), property(P), step(T),
                step(T), addressedBy(C,P), 
                not addressToFunc(P,C,_,_).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), not h(sat(Y),T), step(T).
-h(sat(X),T) :- concern(X), concern(Y), subconcern(X,Y), -h(sat(Y),T), step(T).
h(sat(C),T) :- not -h(sat(C),T), concern(C), step(T).



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


no_all_pos_concern(C,N1,T) :- concern(C), step(T), 
                              N1=#count{P,Com : component(Com),property(P),
                                                possible_rel_pos(Com,P),
                                                addressedBy(C,P)}.

no_act_pos_concern(C,N2,T) :- concern(C), step(T), 
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
%#show sat_formulas/3.
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
%#show no_all_pos_concern/3.
%#show degree_pos_temp/3.

