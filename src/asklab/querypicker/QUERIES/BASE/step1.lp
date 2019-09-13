% ======== SIMPLE EXAMPLE 1 ========
%       -- to be used together with theory*.lp
%          and with step1-BASE.lp
%          (this example uses pessimistic inference)
%
% SYSTEM DESCRIPTION
% Input device 1 can operate in one of slow-mode and fast-mode.
% The SAM determines the mode of operation of input device 1.
% Normally, input device 1 reads inputs with a consistent frequency.
% If the basic type of input device 1 is configured to use
% encrypted memory and fast-mode, then the device will be
% unable to maintain a consistent frequency of reading.
%
% CONFIGURATION
% The SAM and input device 1 are configured to use encrypted 
% memory and secure boot. 
% The basic type of input device 1 is used.
% The SAM is configured to set input device 1 to slow-mode.
%
% Questions:
%   1. Is the functionality concern satisfied?
%   2. Is the functional aspect satisfied?
%   3. Are all aspects satisfied?
% 
% Answers:
%   1. Yes
%   2. Yes (because all concerns and sub-concerns of functional aspect are satisfied)
%   3. Yes (because all aspects are satisfied)

% Enable skeptical inference on concern satisfaction
inference(concerns,pessimistic).


% ------ Output Interface ------

%output(D,property,S) :- last_step(S), -holds(sat_property(A),S), atomic_statement(P,A), descr(P,D).
%output(C,concern,S) :- last_step(S), -holds(sat_concern(C),S),-aspect(C).
%output(C,aspect,S) :- last_step(S), -holds(sat_concern(C),S),aspect(C).
%output("concern-tree",tree,S) :- last_step(S), -holds(sat_all,S).
%
%output_headings("unsatisfied concern/aspect/property","type","step").

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
output(D,property,"-",S) :- last_step(S), -holds(sat(A),S), atomic_statement(P,A), descr(P,D).
output(C,concern,F,S) :- last_step(S), -holds(sat(C,F),S),concern(C),not aspect(C), C!=all.
output(C,aspect,F,S) :- last_step(S), -holds(sat(C,F),S),aspect(C).
output("concern-tree",tree,F,S) :- last_step(S), -holds(sat(all,F),S).

output(C,"concern/aspect (unk)",F,S) :- 
	inference(concerns,skeptical),
	last_step(S), concern(C), relevantToFunc(C,F), 
	not holds(sat(C,F),S),
	not holds(sat(C,F),S).

output_headings("unsatisfied concern/aspect/property","type","function","step").
	