% ------ Output Interface ------

output_headings("Concern","Satisfied","Step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).


output(C,"No",S) :- last_step(S), -h(sat(C),S), concern(C).
output(C,"Yes",S) :- last_step(S), h(sat(C),S), concern(C). 