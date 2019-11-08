
%sol(addr).
sol(all).

% Ontology
subconcern(b1,a1).
subconcern(b0,b1).

addressedBy(a1,x).
addressedBy(a2,x).
addressedBy(a3,x).
addressedBy(a3,y).
addressedBy(b1,y).
addressedBy(b1,z).
addressedBy(b2,z).
addressedBy(b3,z).
addressedBy(a2,z).
addressedBy(b1,t).
addressedBy(b2,t).
addressedBy(b3,t).
addressedBy(a2,t).

property(x).
property(y).
property(z).
property(t).

component(c1).
component(c2).
component(c3).
input(c1,"hasProperty",x).
input(c1,"hasProperty",y).
input(c2,"hasProperty",y).
input(c2,"hasProperty",x).
input(c2,"hasProperty",z).
input(c3,"hasProperty",z).
input(c3,"hasProperty",t).

% Reasoning
count_relations(P,N) :- N=#count{C : addressedBy(C,P)}, property(P), sol(addr).

addrForConcern(P,C) :- property(P), addressedBy(C,P), sol(all).
addrForConcern(P,C) :- addrForConcern(P,C1), subconcern(C,C1), sol(all).
count_relations(P,N) :- N= #count{C : addrForConcern(P,C)}, property(P), sol(all).

componentHasProperty(Com,P) :- input(Com,"hasProperty",P), component(Com), property(P).
truthworthiness_comp(Comp,TWvalue) :- component(Comp), TWvalue= #sum{N,P : count_relations(P,N), property(P), componentHasProperty(Comp,P)}.
higher_TW(C1,C2) :- truthworthiness_comp(C1,TW1), truthworthiness_comp(C2,TW2), TW1 > TW2.
not_highest_TW(C2) :- component(C1),component(C2) ,higher_TW(C1,C2).
highest_TW(C) :- component(C), not not_highest_TW(C).

#show count_relations/2.
#show componentHasProperty/2.
#show truthworthiness_comp/2.
#show highest_TW/1.
#show addrForConcern/2.


