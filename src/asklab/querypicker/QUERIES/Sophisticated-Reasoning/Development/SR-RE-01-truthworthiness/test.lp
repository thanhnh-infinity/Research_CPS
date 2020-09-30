a(3).
b(0).

c(X) :- X = M/N, a(M), b(N), N!=0.
c(M) :- a(M), b(N), N=0.