% =====Ontology============== (Step 1)
relevantToFunc(a1,f).
relevantToFunc(b1,f).
relevantToFunc(b0,f).
relevantToFunc(c1,f).
relevantToFunc(c2,f).

% Order sibling concerns
%order(SC,F,N):-
%    subconcern(C,SC), relevantToFunc(SC,F),
%    N = { SC < SCp : subconcern(C,SCp), relevantToFunc(SCp,F) }.

subconcern(b1,a1).
subconcern(b0,b1).
%subconcern(b0,c1).
%subconcern(b1,c1).
%subconcern(b1,c2).

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


% ======Physical CPS System (step 3)
component(c1).
component(c2).
component(c3).
relation(c1,x,"c1 works x").
relation(c1,y,"c1 works y").
relation(c2,y,"c2 works y").
relation(c2,x,"c2 works x").
relation(c2,z,"c1 works z").
relation(c3,z,"c3 works z").
relation(c3,t,"c1 works t").

% ======Observation for Initial State
obs(x,true).
obs(y,true).
obs(z,true).
obs(t,true).