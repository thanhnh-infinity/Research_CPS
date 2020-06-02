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

