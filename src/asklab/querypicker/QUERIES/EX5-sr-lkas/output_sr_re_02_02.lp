% ------ Output Interface ------

output_headings("Concern","LoCS","Satisfied","Step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).


output(C,LoS,"N",S) :- last_step(S), -h(sat(C),S), likelihood_sat(C,LoS,S).
output(C,LoS,"Y",S) :- last_step(S), h(sat(C),S), likelihood_sat(C,LoS,S).                         



% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
