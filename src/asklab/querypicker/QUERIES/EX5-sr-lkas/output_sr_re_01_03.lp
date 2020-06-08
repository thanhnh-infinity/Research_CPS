% ------ Output Interface ------

output_headings("Action","Step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).

output(A,S) :- occurs(A,S), action(A).




% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
