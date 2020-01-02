% Aspect
aspect(trustworthiness).

% Concern
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
concern(frequency).
concern(controllability).
concern(confidentiality).
concern(integrity).
concern(availability).
concern(controls).
concern(transparency).
concern(availability).
concern(innovation).

concern(encryption).
concern(privacy_policy).
concern(protection).
concern(software_patches).
concern(hardware_patches).
concern(license).
concern(authorization).
concern(roles).
concern(privileges).

% subconcern.
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

%subconcern(physical_security,integrity).
%subconcern(physical_security,availability).
subconcern(physical_security,ultility).

subconcern(predictability,controls).
subconcern(predictability,transparency).
subconcern(predictability,innovation).

subconcern(confidentiality,encryption).
subconcern(confidentiality,privacy_policy).
subconcern(confidentiality,protection).
subconcern(confidentiality,encrypt_method).

subconcern(availability,software_patches).
subconcern(availability,hardware_patches).
subconcern(availability,license).

subconcern(controls,authorization).
subconcern(controls,roles).
subconcern(controls,privileges).

% Property --- Requirements
property(data_encrypted).
property(conn_encrypted).
property(protocol_encrypted).

property(firewall_setup).
property(hidden_backdoor).
property(devices_checked).

property(software_licensed).
property(privacy_standard).

property(algo_AES).
property(algo_RSA).
property(algo_DES).

property(oAuth).
property(two_factors_auth).
property(finger_printing_auth).
property(single_auth).

property(secure_boot).

property(record_video_25fps).
property(record_video_50fps).

property(basic_mode).
property(advanced_mode).

property(devices_accessible_permission).
property(data_accessible_permission).

% Addressed : Relation Properties-Concerns
addressedBy(encryption,data_encrypted).
addressedBy(encryption,conn_encrypted).
addressedBy(encryption,protocol_encrypted).

addressedBy(protection,firewall_setup).
addressedBy(protection,hidden_backdoor).
addressedBy(protection,devices_checked).

addressedBy(privacy_policy,software_licensed).
addressedBy(privacy_policy,privacy_standard).

addressedBy(encrypt_method,algo_AES).
addressedBy(encrypt_method,algo_RSA).
addressedBy(encrypt_method,algo_DES).

addressedBy(authorization,oAuth).
addressedBy(authorization,single_auth).
addressedBy(authorization,two_factors_auth).
addressedBy(authorization,finger_printing_auth).

addressedBy(integrity,secure_boot).

addressedBy(integrity,basic_mode).
addressedBy(integrity,advanced_mode).

addressedBy(frequency,record_video_25fps).
addressedBy(frequency,record_video_50fps).

addressedBy(manageability,devices_accessible_permission).
addressedBy(manageability,data_accessible_permission).

% Component and Relation
component(sam).
component(cam).

relation(cam,data_encrypted,"CAM access to encrypted data").
relation(cam,secure_boot,"CAM use Secure Bot").
relation(cam,devices_checked,"CAM has been checked").
relation(cam,record_video_50fps,"CAM has been recorded 50FPS").
relation(cam,advanced_mode,"CAM used Advanced mode").
relation(cam,devices_accessible_permission,"Have to have permission to access CAM").

relation(sam,data_encrypted,"SAM access to encrypted data").
relation(sam,secure_boot,"SAM use Secure Bot").
relation(sam,software_licensed,"SAM used licensed software").
relation(sam,two_factors_auth,"Access to SAM required 2-factors authentication").
relation(sam,firewall_setup,"Firewall protected SAM").
relation(sam,data_accessible_permission,"Have to have permission to access CAM").

% ======Observation for Initial State
obs(data_encrypted,true).
obs(devices_checked,true).
obs(software_licensed,true).
obs(two_factors_auth,false). % Change here to test
obs(secure_boot,true).
obs(record_video_50fps,true).
obs(advanced_mode,true).
obs(firewall_setup,false). % Change here to test
obs(devices_accessible_permission,true).
obs(data_accessible_permission,true).

