% ------ Output Interface ------

output_headings("Action","Prob. Success of Action","Prob. of State","Step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).

output(A,P,Pr,S) :- occurs(A,S), 
                    prob_success(A,P), 
                    action(A), 
                    h(prob_of_state(Pr),S), 
                    step(S).

output("---Overall---","----Final---",Pr,S) :- h(prob_of_state(Pr),S), last_step(S).


% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
