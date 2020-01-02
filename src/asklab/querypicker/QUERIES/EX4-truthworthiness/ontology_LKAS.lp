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

subconcern(physical_security,integrity).
subconcern(physical_security,availability).
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
property(connection_encrypted).
property(protocol_encrypted).

property(firewall_setup).
property(hidden_backdoor).
property(devices_checked).

property(software_licensed).
property(privacy_standard).

property(algo_AES_encryption).
property(algo_RSA_encryption).
property(algo_DES_encryption).

property(oAuth).
property(two_factors_auth).
property(finger_printing_auth).
property(single_auth).


% Addressed : Relation Properties-Concerns
addressedBy(encryption,data_encrypted).
addressedBy(encryption,connection_encrypted).
addressedBy(encryption,protocol_encrypted).

addressedBy(protection,firewall_setup).
addressedBy(protection,hidden_backdoor).
addressedBy(protection,devices_checked).

addressedBy(privacy_policy,software_licensed).
addressedBy(privacy_policy,privacy_standard).

addressedBy(encrypt_method,algo_AES_encryption).
addressedBy(encrypt_method,algo_RSA_encryption).
addressedBy(encrypt_method,algo_DES_encryption).

addressedBy(authorization,oAuth).
addressedBy(authorization,single_auth).
addressedBy(authorization,two_factors_auth).
addressedBy(authorization,finger_printing_auth).

% Component and Relation
component(sam).
component(cam).
