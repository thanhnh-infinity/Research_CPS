% Step 3  -- to be used together with step3.lp
% A cyberattack has occurred and hacked the SAM to switch 
% input device 1 to fast-mode.
% The attack affects the SAM and its effect on the SAM cannot 
% be reversed unless a patch is applied to the SAM. The SAM
% forces the SAM to switch input device 1 to slow-mode.
% We want to know if there is a mitigation and, if so, which one.
%
% Outcome:
%   * Replacing the basic input device 1 with the advanced type solves the
%     problem. The advanced input device 1 can operate in fast-mode
%     with encrypted memory enabled.
%   * Patching the SAM is another mitigation, but has an 80% probability of success.
%
% Questions:
%   1. Is the functionality concern satisfied now?
%   2. Is the functional aspect satisfied now?
%   3. Are all aspects satisfied now?
%   4. What is the mitigation?
% 
% Answers:
%   1. Yes (because the advanced input device 1 can operate
%           in fast-mode without compromising functionality)
%   2. Yes (because all concerns and sub-concerns of functional
%           aspect are satisfied)
%   3. Yes (because all aspects are satisfied)
%   4a. Replace the basic input device 1 with the advanced one
%   4b. Patch the SAM

%prob_success(disable("using_basic_input1"),95).
prob_success(patch(sam),80).
