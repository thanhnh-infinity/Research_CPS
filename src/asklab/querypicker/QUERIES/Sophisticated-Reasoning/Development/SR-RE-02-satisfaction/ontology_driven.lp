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
addressedBy(C,P) :- property(P), concern(C), 
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


%=============================================================
%==================EXTENED ONTOLOGY===========================
%=============================================================

% Component
component(Co)           :- input(Co,"rdf:type","cpsf:Component").

% Possible Relations between Components and Properties
relation(Co,P)          :- component(Co), property(P),
                           input(Co,"cpsf:relateToProperty",P).


% Possible Positive Impacts Component-Property to Concern
component_property(CP)        :- input(CP,"rdf:type","cpsf:Component_Property").
confComponent(CP,CO)          :- component_property(CP), component(CO),
                                 input(CP,"cpsf:confComponent",CO).
confProperty(CP,P)            :- component_property(CP), property(P),
                                 input(CP,"cpsf:confProperty",P).
positiveImpactTo(CP,C)        :- component_property(CP), concern(C),
                                 input(CP,"cpsf:positiveImpactTo",C).
possible_impacts_pos(CO,P,C)  :- component(CO), concern(C), property(P), 
                                 component_property(CP), confComponent(CP,CO),
                                 confProperty(CP,P), positiveImpactTo(CP,C).                              

%=============================================================
%==================INITIAL CONFIGURATION======================
%=============================================================
init_active_com_pro(IACP)     :- input(IACP,"rdf:type","cpsf:InititalActiveComponentsProperties").
active_com_pro(ACP)           :- input(ACP,"rdf:type","cpsf:ActiveComponentProperty").
includesActivation(IACP,ACP)  :- init_active_com_pro(IACP), active_com_pro(ACP),
                                 input(IACP,"cpsf:includesActivation",ACP).

init_active_com(ACP)          :- init_active_com_pro(IACP), inital_active_select(IACP),
                                 active_com_pro(ACP), includesActivation(IACP,ACP).           


setUpForComponent(IAC,CO)     :- init_active_com(IAC), component(CO),
                                 input(IAC,"cpsf:setUpForComponent",CO).
activeToProperty(IAC,P)       :- init_active_com(IAC), property(P),
                                 input(IAC,"cpsf:activeToProperty",P).
active(CO,P)                  :- component(CO), property(P), init_active_com(IAC),
                                 setUpForComponent(IAC,CO), activeToProperty(IAC,P).

% Set up case for Properties Observation
initial_configuration(IC)     :- input(IC,"rdf:type","cpsf:InitialConfiguration").
obsFalse(IC,P)                :- initial_configuration(IC), property(P),
                                 intial_conf_select(IC), input(IC,"cpsf:obsFalse",P).
obs(P,false)                  :- obsFalse(IC,P), initial_configuration(IC), 
                                 property(P), intial_conf_select(IC).
obs(P,true)                   :- not obs(P,false), property(P).

%=============================================================
%#show init_active_com/1.