%%%%%%%
% Satisfaction Theory + Positive Impacts Degree
%%%%%%%


step(0).

%-------The Ontology---------------------
% concern 
aspect(trustworhtiness).

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

addressedBy(protection,firewall_setup).
addressedBy(protection,ip_filtering).


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
suppBy(advanced_mode,operation_mode,2).

%--- For Energy_Mode
requirement(saving_mode).
requirement(powerful_mode).
requirement(normal_mode).

obs(saving_mode,true).
obs(powerful_mode,true).
obs(normal_mode,true).

suppBy(saving_mode,energy_mode,1).
suppBy(powerful_mode,energy_mode,2).
suppBy(normal_mode,energy_mode,2).

% Component
%---- Define component ----
component(sam).
component(cam).
component(battery).
%---- Relation to property----
relation(sam,data_encrypted).
relation(sam,algo_RSA).
relation(sam,firewall_setup).
relation(sam,secure_boot).

relation(cam,ip_filtering).
relation(cam,data_encrypted).
relation(cam,secure_boot).

%---- Relation to property requirement ----
relation(sam,basic_mode).
relation(sam,finger_printing).
relation(cam,advanced_mode).
relation(battery,normal_mode).

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
deg(advanced_mode,operation_mode,8,0).
deg(basic_mode,operation_mode,6,0).
deg(saving_mode,energy_mode,2,0).
deg(normal_mode,energy_mode,7,0).
deg(powerful_mode,energy_mode,9,0).
deg(finger_printing,auth_strategies,7,0).
deg(two_factors,auth_strategies,6,0).
deg(oauth,auth_strategies,5,0).
deg(opt_code,auth_strategies,3,0).
deg(email_verify,auth_strategies,3,0).
deg(ip_check,auth_strategies,3,0).

%%%%% --- Default Assignment PID values for Property NOT have any supports --
deg(secure_boot,integrity,6,0).
deg(firewall_setup,verification,7,0).
deg(ip_filtering,verification,3,0).
deg(algo_RSA,encryption,8,0).
deg(algo_AES,encryption,6,0).
deg(protocol_encrypted,encryption,10,0).
deg(data_encrypted,encryption,10,0).

%------------------------------------------------------------------
%---- Reasoning Likelihood of Concerns Satisfaction ---------------
%-- Asumming -- Se phai bo di khi co cach tinh Property
degree_pos(encryption,80,0).
degree_pos(verification,21,0).
degree_pos(integrity,12,0).
degree_pos(authorization,70,0).

degree_pos(manageability,1,0).
degree_pos(dissociability,1,0).
degree_pos(severity,1,0).
degree_pos(controllability,1,0).
degree_pos(frequency,1,0).
degree_pos(availability,1,0).
degree_pos(transparency,1,0).
degree_pos(innovation,1,0).
degree_pos(ultility,1,0).
degree_pos(authentication,1,0).
degree_pos(all,1,0).
degree_pos(trustworthiness,1,0).
degree_pos(safety,1,0).
degree_pos(reliability,1,0).
degree_pos(security,1,0).
degree_pos(resilience,1,0).
degree_pos(privacy,1,0).

degree_pos(functional_safety,1,0).
degree_pos(cyber_security,1,0).
degree_pos(physical_security,1,0).
degree_pos(predictability,1,0).

degree_pos(confidentiality,1,0).
degree_pos(controls,1,0).


%--- Reasoning Algorithm ----
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
