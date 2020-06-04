%-----------The CPS ontology -----------------
% aspect
property(P)     :- input(P,"rdf:type","cpsf:Property").
descr(P,D)      :- input(P,"rdfs:comment",D).
concern(C)      :- input(C,"rdf:type","cpsf:Concern").
aspect(A)       :- input(A,"rdf:type","cpsf:Aspect").
subconcern(S,O) :- input(S,"cpsf:includesConcern",O).

% every aspect is a concern
concern(A) :- aspect(A).

% meta-aspect "all", which is a parent of every aspect
concern(all).
subconcern(all,A) :- aspect(A).

% Property addresses a concern
addressedBy(P,C) :- property(P), concern(C), 
                    input(P,"cpsf:addConcern",C).


% Formulas
formulas(For)    :- input(For,"rdf:type","cpsf:Formulas").

% Properties memeber of formulas
member(P,For)    :- property(P), formulas(For),
                    input(P,"cpsf:memberOf",For).

% Decompostion Function
decomposition(DF)       :- input(DF,"rdf:type","cpsf:DecompositionFunction"). 
func_dec(DF,C)          :- decomposition(DF), concern(C),
                           input(DF,"cpsf:decomposition_function_of",C).
add_func(For,DF)        :- decomposition(DF), formulas(For),
                           input(For,"cpsf:addressToFunc",DF).
addressToFunc(C,DF,For) :- concern(C), decomposition(DF), formulas(For),
                           func_dec(DF,C), add_func(For,DF).


% Component
component(Co)           :- input(Co,"rdf:type","cpsf:Component").

% Possible Relations between Components and Properties
relation(Co,P)          :- component(Co), property(P),
                           input(Co,"cpsf:relateToProperty",P).

%=============================================================
%==================EXTENED ONTOLOGY===========================
%=============================================================

% ====Component


%=============================================================
%==================INITIAL CONFIGURATIOn======================
%=============================================================

#show relation/2.