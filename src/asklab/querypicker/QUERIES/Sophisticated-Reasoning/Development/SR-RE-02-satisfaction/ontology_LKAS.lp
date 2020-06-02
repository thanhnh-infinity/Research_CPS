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

% Formulas
formulas(1..10).

member(finger_printing,1).
member(two_factors,2).
member(iris_scan,3).
member(oauth,4).
member(opt_code,4).
member(oauth,5).
member(email_verify,5).
member(ip_check,5).

member(advanced_mode,6).
member(basic_mode,7).

member(saving_mode,8).
member(powerful_mode,9).
member(normal_mode,10).

func_dec(sign_in_func,authorization).
func_dec(operation_func,integrity).
func_dec(energy_func,integrity).

addressToFunc(authorization,sign_in_func,1).
addressToFunc(authorization,sign_in_func,2).
addressToFunc(authorization,sign_in_func,3).
addressToFunc(authorization,sign_in_func,4).
addressToFunc(authorization,sign_in_func,5).

%--- For Operation_Mode
addressToFunc(integrity,operation_func,6).
addressToFunc(integrity,operation_func,7).

%--- For Energy_Mode
addressToFunc(integrity,energy_func,8).
addressToFunc(integrity,energy_func,9).
addressToFunc(integrity,energy_func,10).

%=============================================================
%==================EXTENED ONTOLOGY===========================
%=============================================================

% ====Component
%---- Define component ----
component(sam).
component(cam).
component(battery).

%---- Possible Relations Between Componentns and Properties ----
% Possible relation cam
relation(cam,algo_AES).
relation(cam,algo_RSA).
relation(cam,algo_DES).
relation(cam,conn_encrypted).
relation(cam,data_encrypted).
relation(cam,protocol_encrypted).
relation(cam,ip_filtering).
relation(cam,mac_check).
relation(cam,advanced_mode).
relation(cam,basic_mode).
relation(cam,secure_boot).
relation(cam,trusted_auth_device).
relation(cam,trusted_environment).
relation(cam,iris_scan).

% Possible relation sam
relation(sam,algo_AES).
relation(sam,algo_RSA).
relation(sam,algo_DES).
relation(sam,conn_encrypted).
relation(sam,data_encrypted).
relation(sam,protocol_encrypted).
relation(sam,ip_filtering).
relation(sam,firewall_setup).
relation(sam,mac_check).
relation(sam,advanced_mode).
relation(sam,basic_mode).
relation(sam,secure_boot).
relation(sam,finger_printing).
relation(sam,two_factors).
relation(sam,iris_scan).
relation(sam,oauth).
relation(sam,opt_code).
relation(sam,email_verify).
relation(sam,ip_check).
relation(sam,trusted_environment).

% Possible relation battery
relation(battery,powerful_mode).
relation(battery,normal_mode).
relation(battery,saving_mode).
relation(battery,trusted_environment).

%---- Define Possible Positive Impact Relation of each component
% possible pos impact sam
possible_impacts_pos(sam,data_encrypted,encryption).
possible_impacts_pos(sam,conn_encrypted,encryption).
possible_impacts_pos(sam,protocol_encrypted,encryption).
possible_impacts_pos(sam,algo_RSA,encryption).
possible_impacts_pos(sam,algo_AES,encryption).
possible_impacts_pos(sam,firewall_setup,verification).
possible_impacts_pos(sam,mac_check,verification).
possible_impacts_pos(sam,secure_boot,integrity).
possible_impacts_pos(sam,advanced_mode,integrity).
possible_impacts_pos(sam,iris_scan,authorization).
possible_impacts_pos(sam,two_factors,authorization).
possible_impacts_pos(sam,finger_printing,authorization).
possible_impacts_pos(sam,trusted_environment,authorization).

% possible pos impact cam
possible_impacts_pos(cam,algo_RSA,encryption).
possible_impacts_pos(cam,data_encrypted,encryption).
possible_impacts_pos(cam,conn_encrypted,encryption).
possible_impacts_pos(cam,protocol_encrypted,encryption).
possible_impacts_pos(cam,mac_check,verification).
possible_impacts_pos(cam,secure_boot,integrity).
possible_impacts_pos(cam,advanced_mode,integrity).
possible_impacts_pos(cam,trusted_auth_device,authorization).
possible_impacts_pos(cam,trusted_environment,authorization).

% possible pos impact bat
possible_impacts_pos(battery,powerful_mode,integrity).
possible_impacts_pos(battery,trusted_environment,authorization).
%=============================================================