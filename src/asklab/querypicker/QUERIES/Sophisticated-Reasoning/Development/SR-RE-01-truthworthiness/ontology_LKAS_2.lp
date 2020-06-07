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
concern(authentication).
concern(roles).
concern(privileges).
concern(permissions).

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

subconcern(physical_security,ultility).

subconcern(predictability,controls).
subconcern(predictability,transparency).
subconcern(predictability,innovation).

subconcern(confidentiality,encryption).
subconcern(confidentiality,privacy_policy).
subconcern(confidentiality,protection).

subconcern(availability,software_patches).
subconcern(availability,hardware_patches).
subconcern(availability,license).

subconcern(controls,authentication).
subconcern(controls,identity).

subconcern(identity,authorization).

% Property --- Requirements
property(data_encrypted).
property(conn_encrypted).
property(protocol_encrypted).

property(firewall_setup).
property(hidden_backdoor).
property(data_filtering).

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

property(devices_access_permission).
property(data_access_permission).

% Addressed : Relation Properties-Concerns
addressedBy(encryption,data_encrypted).
addressedBy(encryption,conn_encrypted).
addressedBy(encryption,protocol_encrypted).
addressedBy(encryption,algo_AES).
addressedBy(encryption,algo_RSA).

addressedBy(protection,firewall_setup).
addressedBy(protection,hidden_backdoor).
addressedBy(protection,data_filtering).

addressedBy(privacy_policy,software_licensed).
addressedBy(privacy_policy,privacy_standard).

addressedBy(authentication,oAuth).
addressedBy(authentication,single_auth).
addressedBy(authentication,two_factors_auth).
addressedBy(authentication,finger_printing_auth).

addressedBy(integrity,secure_boot).

addressedBy(integrity,basic_mode).
addressedBy(integrity,advanced_mode).

addressedBy(frequency,record_video_25fps).
addressedBy(frequency,record_video_50fps).

addressedBy(authorization,devices_access_permission).
addressedBy(authorization,data_access_permission).

% Component and Relation
component(sam).
component(cam).

relation(cam,data_encrypted).
relation(cam,secure_boot).
relation(cam,data_filtering).
%relation(cam,record_video_50fps,"CAM has been recorded 50FPS").
relation(cam,advanced_mode).
relation(cam,devices_access_permission).

relation(sam,data_encrypted).
relation(sam,secure_boot).
relation(sam,software_licensed).
relation(sam,two_factors_auth).
relation(sam,firewall_setup).
relation(sam,data_access_permission).



