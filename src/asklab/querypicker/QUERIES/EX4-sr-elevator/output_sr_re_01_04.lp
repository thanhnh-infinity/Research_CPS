% ------ Output Interface ------

output_headings("Unsatisfied concern/aspect/property","type","function","step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).

output(C,concern,"-",S) :- last_step(S), -h(sat(C),S), concern(C).
output(C,aspect,"-",S) :- last_step(S), -h(sat(C),S), aspect(C).
output(C,concern,F,S) :- last_step(S), -h(sat(C,F),S),concern(C), not aspect(C), C!=all.
output(C,aspect,F,S) :- last_step(S), -h(sat(C,F),S), aspect(C).
output("concern-tree",tree,F,S) :- last_step(S), -h(sat(all,F),S).
output("concern-tree",tree,"-",S) :- last_step(S), -h(sat(all),S).

output(P,property,"-",S) :- last_step(S), -h(P,S), property(P).


% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
