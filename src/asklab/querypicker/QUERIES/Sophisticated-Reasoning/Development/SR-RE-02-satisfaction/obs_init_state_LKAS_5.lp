%==================INITIAL OBSERVATION===========================
obs(data_encrypted,true).
obs(conn_encrypted,true).
obs(protocol_encrypted,true).
obs(algo_AES,true).
obs(algo_RSA,true).
obs(algo_DES,true).
obs(firewall_setup,true).
obs(ip_filtering,true).
obs(mac_check,true).
obs(secure_boot,true).
obs(trusted_auth_device,true).
obs(trusted_environment,true).
obs(finger_printing,true).
obs(two_factors,true).
obs(iris_scan,true).
obs(oauth,true).
obs(opt_code,true).
obs(email_verify,true).
obs(ip_check,true).
obs(advanced_mode,true).
obs(basic_mode,true).
obs(saving_mode,true).
obs(powerful_mode,true).
obs(normal_mode,true).

%========== Current Active Between Components and Properties ==========
active(sam,data_encrypted).
active(sam,algo_RSA).
active(sam,firewall_setup).
active(sam,advanced_mode).
active(sam,secure_boot).
active(sam,trusted_environment).
active(sam,finger_printing).

active(cam,ip_filtering).
active(cam,data_encrypted).
active(cam,conn_encrypted).
active(cam,advanced_mode).
active(cam,secure_boot).
active(cam,trusted_auth_device).


% Change to see the different of LoS values
active(battery,saving_mode).
active(battery,trusted_environment).