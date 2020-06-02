%==================INITIAL OBSERVATION===========================
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
obs(finger_printing,false).
obs(two_factors,false).
obs(iris_scan,false).
obs(oauth,false).
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
active(sam,secure_boot).

active(cam,ip_filtering).
active(cam,data_encrypted).
active(cam,conn_encrypted).
active(cam,secure_boot).
active(cam,trusted_auth_device).

% Change to see the different of LoS values
active(sam,finger_printing).
active(sam,basic_mode).
active(cam,basic_mode).
active(battery,powerful_mode).