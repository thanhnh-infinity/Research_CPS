root(a).

node(b).
node(c).
node(d).

sub(a,b).
sub(a,c).
sub(a,d).

value(b,4).
value(c,2).
value(d,3).

value(a,1).
value(X,M) :- root(X), {V1*V : node(N),sub(X,N),value(N,V1),value(X,V)}.
                