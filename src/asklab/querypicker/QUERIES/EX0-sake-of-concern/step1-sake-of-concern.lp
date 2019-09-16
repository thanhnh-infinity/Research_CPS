%       -- to be used together with theory*.lp
%          and with step1-BASE.lp

%
% This example shows the formalization's capability to answer a question
% such as:
%
%     What have you done across the system for the sake of cybersecurity?
%

% How to answer:
%  Roughly speaking, the answers to the question
%  are all properties "attached" to cybersecurity and
%  all properties impacting (possibly transitive) sub-concerns
%  of cybersecurity, or cybersecurity itself.
%  
%  Solution:
%    1. Find every impact rule r such that <r cpsf:addressesConcern c>
%       and <r cpsf:addressesPolarity positive>
%       and c is cybersecurity or one of its (possibly transitive) sub-concerns
%       and <r cpsf:addressesAtFunc f>.
%    2. Return every condition+polarity of r and the function f.
%
% The example produces the answer:
%
%    encrypted_mem_input1,pos,cpsf:bc1
%    encrypted_mem_sam,pos,cpsf:bc1
%    sec_boot_input1,pos,cpsf:bc1
%    sec_boot_sam,pos,cpsf:bc1
%
% Notice that, while none of the above requirements impact cybersecurity
% directly, they impact confidentiality and integrity, which are
% subconcerns of cybersecurity. Hence the answer produced.
%

% The question is about confidentiality
target_concern("cpsf:Cybersecurity").

% ASP encoding of query
for_sake_of_target_concern(Q,CondP,F) :-
	rule(Rule),
	target_concern(PC),
	tc0(subconcern(PC,C)),
	addressesConcern(Rule,C),
	addressesPolarity(Rule,pos),
	addressesAtFunc(Rule,F),
	hasCondition(Rule,Cond),
	conditionProperty(Cond,Q),
	conditionPolarity(Cond,CondP).

% ------ Output Interface ------

output(Q,CondP,F,C) :- target_concern(C), for_sake_of_target_concern(Q,CondP,F).

output_headings("property","polarity","function","for sake of concern").
