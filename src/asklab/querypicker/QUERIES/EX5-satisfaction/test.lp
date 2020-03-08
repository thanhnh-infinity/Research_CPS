-h(conn_encrypted,by(wind_sensor,socket_conn),T) :- h(use(wind_sensor,socket_conn),T), h(socket_conn,T), step(T).
-h(conn_encrypted,by(d,p),0).
-h(a,0).

h(conflict(C,type_1),T) :- -h(P2,by(Com,P),T), h(use(Com,P),T), h(P,T), prop(P2), prop(P), P!=P2 ,  addBy(P2,C), concern(C), comp(Com), step(T).
-h(P,T) :- -h(P,by(_,_),T), step(T).

%-h(P2,constraint,T) :- h(use(Com,P),T), h(P,T), comp(Com), prop(P), prop(P2), concern(C), addBy(P2,C), P!=P2.

addBy(conn_encrypted,encryption).
addBy(a,encryption).
concern(encryption).
step(0).
prop(conn_encrypted).
prop(socket_conn).
prop(a).

h(use(wind_sensor,socket_conn),0).
h(socket_conn,0).
comp(wind_sensor).


comp(d).
prop(p).

#show h/2.
%#show -h/3.