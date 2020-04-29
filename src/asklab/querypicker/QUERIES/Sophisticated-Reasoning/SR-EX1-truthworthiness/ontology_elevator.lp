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
concern(human_safety).
concern(cyber_security).
concern(physical_security).
concern(predictability).
concern(manageability).
concern(dissociability).

concern(hazard).

concern(severity).
concern(frequency).
concern(controllability).
concern(confidentiality).
concern(integrity).
concern(physical_integrity).
concern(availability).
concern(stability).
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
concern(functionality).

% subconcern.
subconcern(trustworthiness,safety).
subconcern(trustworthiness,reliability).
subconcern(trustworthiness,security).
subconcern(trustworthiness,resilience).
subconcern(trustworthiness,privacy).

subconcern(safety,functional_safety).
subconcern(safety,human_safety).

subconcern(security,cyber_security).
subconcern(security,physical_security).

subconcern(privacy,predictability).
subconcern(privacy,manageability).
subconcern(privacy,dissociability).

subconcern(functional_safety,hazard).

subconcern(hazard,severity).
subconcern(hazard,frequency).
subconcern(hazard,controllability).

subconcern(cyber_security,confidentiality).
subconcern(cyber_security,integrity).
subconcern(cyber_security,availability).

subconcern(physical_security,ultility).
subconcern(physical_security,physical_integrity).
subconcern(physical_security,stability).

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
subconcern(stability,functionality).

% Property --- Requirements
property(maintenance_regularly).
property(control_speed).
property(record_25fps).
property(send_actions).
property(control_pulley).
property(pulley_release).
property(pulley_clench).
property(moving_up).
property(moving_down).
property(halting).
property(control_moving).
property(communicate_with_other_comp).
property(detect_No_passenger).


% Addressed : Relation Properties-Concerns
addressedBy(controllability,maintenance_regularly).
addressedBy(frequency,maintenance_regularly).
addressedBy(controllability,control_speed).
addressedBy(human_safety,control_speed).
addressedBy(integrity,record_25fps).
addressedBy(integrity,send_actions).
addressedBy(functionality,send_actions).
addressedBy(functionality,control_pulley).

addressedBy(physical_integrity,pulley_release).
addressedBy(physical_integrity,pulley_clench).
addressedBy(physical_integrity,moving_up).
addressedBy(physical_integrity,moving_down).
addressedBy(physical_integrity,halting).

addressedBy(functionality,control_moving).
addressedBy(availability,communicate_with_other_comp).
addressedBy(functionality,communicate_with_other_comp).
addressedBy(manageability,communicate_with_other_comp).
addressedBy(manageability,detect_No_passenger).


% Component and Relation
component(cp).
component(er).
component(pf).
component(ec).
component(escam).

relation(cp,maintenance_regularly,"cp maintenance").
relation(cp,communicate_with_other_comp,"cp communicate").

relation(er,control_speed,"er control speed").
relation(er,send_actions,"er send actions").
relation(er,communicate_with_other_comp,"er communicate").

relation(pf,maintenance_regularly,"PF maintenance").
relation(pf,control_speed,"PF control speed").
relation(pf,control_pulley,"PF control pulley").
relation(pf,pulley_release,"PF release").
relation(pf,pulley_clench,"PF clench").
relation(pf,communicate_with_other_comp,"PF communicate").

relation(ec,maintenance_regularly,"EC maintenance").
relation(ec,halting,"PF halts").
relation(ec,moving_down,"EC downd").
relation(ec,moving_up,"EC up").
relation(ec,control_moving,"EC moving").
relation(ec,communicate_with_other_comp,"EC communicate").

relation(escam,record_25fps,"ESCAM maintenance").
relation(escam,communicate_with_other_comp,"ESCAM").
relation(escam,detect_No_passenger,"ESCAM").

% ======Observation for Initial State
obs(maintenance_regularly,true).
obs(control_speed,false).
obs(record_25fps,true).
obs(send_actions,true).
obs(control_pulley,true).
obs(pulley_release,true).
obs(pulley_clench,true).
obs(moving_up,true).
obs(moving_down,true).
obs(halting,true).
obs(control_moving,true).
obs(communicate_with_other_comp,true).
obs(detect_No_passenger,false).
obs(availablePatch(control_speed),true).
