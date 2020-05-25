% ------ Output Interface ------

output_headings("Query response","Component","Positive TW val","Negative TW val","Distance","step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).

output("Most trustworthy component",C,TWp,TWn,D,S) :- highest_TW_comp(C,S), step(S), last_step(S), 
														  tw_good_comp(C,TWp,S), tw_bad_comp(C,TWn,S),
														  distance(C,D,S).
output("Lest trustworthy component",C,TWp,TWn,D,S) :- lowest_TW_comp(C,S), step(S), last_step(S), 
														  tw_good_comp(C,TWp,S), tw_bad_comp(C,TWn,S),
														  distance(C,D,S).

% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
