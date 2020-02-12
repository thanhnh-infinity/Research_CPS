step(0).

root(a).

node(a).

node(b).
node(c).
node(d).
node(b1).
node(b2).
node(c1).
node(c2).
node(d1).
node(d2).
node(d3).

sub(a,b).
sub(a,c).
sub(a,d).

sub(b,b1).
sub(b,b2).
sub(c,c1).
sub(c,c2).
sub(d,d1).
sub(d,d2).
sub(d,d3).

value(b,4,0).
value(c,2,0).
value(d,3,0).

value(b1,6,0).
value(c1,7,0).
value(d1,8,0).

value(b2,2,0).
value(c2,1,0).
value(d2,1,0).


value(d3,2,0).


order(SC,C,N) :- sub(C,SC), N = { SC < SCp : sub(C,SCp)}.
has_sub(S) :- sub(S,SC).
-has_sub(C) :- node(C), not has_sub(C).

likelihood_sat_sub(C,1,T) :- step(T), node(C), -has_sub(C). 

likelihood_sat(C,N,T) :- step(T), node(C), likelihood_sat_sub(C,N1,T), value(C,N2,T), N=N1*N2.

likelihood_sat_sub_aux(C,0,X,T) :- step(T), sub(C,SC), order(SC,C,0), likelihood_sat(SC,X,T).

likelihood_sat_sub_aux(C,N,Value,T) :- step(T), sub(C,SC), order(SC,C,N), likelihood_sat(SC,Y,T),
                                       likelihood_sat_sub_aux(C,N-1,X,T), Value=X*Y. 

likelihood_sat_sub(C,X,T) :- step(T), node(C), likelihood_sat_sub_aux(C,N,X,T), not likelihood_sat_sub_aux(C,N+1,_,T).

#show order/3.
%#show -has_sub/1.
#show likelihood_sat_sub/3.
#show likelihood_sat/3.
#show likelihood_sat_sub_aux/4.