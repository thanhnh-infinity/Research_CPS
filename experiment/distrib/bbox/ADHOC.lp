rel1(X,Y) :- input(X,"hashowl:def3146364d5c003c703a3f479c21fa44c4d59e4dce980409922cff2e41d400fd",Y).

t(X,Y) :-
	input(X,"rdf:type",Y).

s(X,Y) :-
	input(X,"rdfs:subClassOf",Y).


p(I) :- t(I,_).

-rel2(X,Y2) :-
	rel2(X,Y1),
	rel1(_,Y1),
	rel1(_,Y2),
	Y1 != Y2.

rel2(X,Y) :-
	rel1(X,Y).

rel2(X,Y) :-
	t(X,Y),
	rel2(Y,Y),
	not -rel2(X,Y).

rel2(X,Y) :-
	s(X,Y),
	rel2(Y,Y),
	not -rel2(X,Y).

output_headings("a","b").

output(X,Y) :-
	p(X),
	rel2(X,Y).

#show output_headings/2.
#show output/2.
