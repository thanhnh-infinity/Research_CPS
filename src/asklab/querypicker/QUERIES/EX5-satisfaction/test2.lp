step(0).

prop(p1).
prop(p2).
prop(p3).
prop(p4).

{h(p1,0);h(p2,0);h(p3,0);h(p4,0)}.

%-h(p2,0) :- h(p1,0), h(p3,0).

-h(P,T) :- 1{h(P1,T) : prop(P1), P1 != P}, prop(P), step(T).

#show h/2.
#show -h/2.