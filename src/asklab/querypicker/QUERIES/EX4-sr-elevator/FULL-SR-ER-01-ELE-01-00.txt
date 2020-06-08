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
%#show obs/1.% Input Changes
intial_conf_select("cpsf:ele_sr_er_01_initial_conf_0").
inital_active_select("cpsf:ele_sr_er_01_active_component_properties_case_0").
obs(availablePatch("cpsf:Control_Speed"),true).
obs(availablePatch("cpsf:Detect_Up_11"),true).
%===========================================================================%=====REASONING TRUTHWORTHINESS with STEP======

% =====Configuration=========
%sol(addr).
sol(all).

% =====State of CPS System===
step(0).

%----------------------------------------------
%=====REASONING TRUTHWORTHINESS with STEP======
%----------------------------------------------

% -- Step 2 : Representation the property P in initial state of CPS 
holds(P,0) :- obs(P,true), property(P).
-holds(P,0) :- obs(P,false), property(P).

% -- Step 3: Check addresses links
addrForConcern(P,C) :- property(P), 
					             addressedBy(C,P), 
					             sol(all).
addrForConcern(P,C) :- addrForConcern(P,C1), 
                       subconcern(C,C1), 
                       sol(all).
                       
% -- Step 4 [1,2]: Reasoning a component C has good/bad property P at step S.
compGoodProp(Com,P,S) :- relation(Com,P), holds(P,S), 
						             component(Com), property(P), step(S).
compBadProp(Com,P,S)  :- component(Com), property(P), step(S),
                         relation(Com,P), -holds(P,S).

% -- Step 5: Compute the tw_property: total number of links to the concerns that are addressed by and related to property P
tw_property(P,N) :- N=#count{C : addressedBy(C,P)}, 
                    property(P), sol(addr).
tw_property(P,N) :- N=#count{C : addrForConcern(P,C)}, 
                    property(P), sol(all).

% -- Step 6: Compute the good trustworthiness value of component C
tw_good_comp(Comp,TWvalue,S) :- component(Comp), step(S),
								                TWvalue = #sum{N,P : tw_property(P,N), property(P), compGoodProp(Comp,P,S)}.

% -- Step 7: Compute the bad trustworthiness value of component C
tw_bad_comp(Comp,TWvalue,S)  :- component(Comp), step(S),
                                TWvalue = #sum{N,P : tw_property(P,N), property(P), compBadProp(Comp,P,S)}.

% -- Step 7-1 : Middle layer: Representation good/bad tw if not exists
tw_good_comp(Comp,0,S)  :- not tw_good_comp(Comp,_,S), 
                           component(Comp), step(S).
tw_bad_comp(Comp,0,S)   :- not tw_bad_comp(Comp,_,S), 
                           component(Comp), step(S).

% -- Step 8: Ordering and result
distance(C,D,S) :- component(C), step(S), tw_good_comp(C,TWp,S),
                   tw_bad_comp(C,TWn,S), D = TWp-TWn. 

% -- Step 9: Find the highest/lowest TW value
highest_TW_comp(C,S) :- component(C), step(S), distance(C,M,S),
                        M == #max{N:distance(_,N,S)}.
lowest_TW_comp(C,S)  :- component(C), step(S), distance(C,M,S),
                        M == #min{N:distance(_,N,S)}.
%----------------------------------------------


% ====== SHOW ========


% ------ Output Interface ------

output_headings("Query response","Component","Positive TW val","Negative TW val","Distance","step").

% Support : Identify the last step in the input
last_step(S) :- step(S), S2=S+1, not step(S2).

output("Most trustworthy component",C,TWp,TWn,D,S) :- highest_TW_comp(C,S), step(S), last_step(S), 
														  tw_good_comp(C,TWp,S), tw_bad_comp(C,TWn,S),
														  distance(C,D,S).
output("Lest trustworthy component",C,TWp,TWn,D,S) :- lowest_TW_comp(C,S), step(S), last_step(S), 
														  tw_good_comp(C,TWp,S), tw_bad_comp(C,TWn,S),
														  distance(C,D,S).

% ====== SHOW ========
%#show output_headings/6.
%#show output/6.
