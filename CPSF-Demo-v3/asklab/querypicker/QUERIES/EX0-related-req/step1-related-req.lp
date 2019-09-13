%       -- to be used together with theory*.lp
%          and with step1-BASE.lp

% Reason about relatedness of requirements while reasoning pessimistically 
% about concerns, i.e. concerns default to unsatisfied.
%
% For illustration purposes, we consider as relevant only the following concerns
% and their ancestors:
%  * Confidentiality
%  * Functionality
%  * Integrity
%
% The business case, bc1, is refined into use cases uc1 and uc2.
% At the business case level, confidentiality is addressed by the use
% of encrypted memory in SAM.
% At the level of use case uc1, confidentiality is addressed by the use
% of AES-256 encryption of memory in SAM.

%
% The example shows that, under this reasoning mode, the (relevant portion of the)
% entire concern tree is satisfied. That is due to the fact that the three
% above concerns are addressed by requirements that are satisfied.  

% Enable skeptical inference on concern satisfaction
inference(concerns,pessimistic).

% ------ Initial state of the CPS ------

% ---(Additional) Observations
obs(sat("encrypted_mem_sam_aes256"),true).


% ------ Output Interface ------

output(R2,R1) :- related(R1,R2).

output_headings("Lower-level requirement","Higher-level requirement related to it").
