i = 0;                                
j = 2*pi;           
m1 = pi/200;
a = 0;
% pcLineCropped(1,:) = pcLineCropped(1,:)-2000; %2000 is displacement from z-axis in this case
% pcLineCroppedOriginal = pcLineCropped;

% This function takes the data gathered from nonzero theta values and
% rotates about the Z axis as the stepper motor moves.
% This file will be edited to take in the subsequent images of the scan set

for n1 = i:m1:j
a = a+1; % Image filename index (used at top of PCconversion)

    PCconversion;
    
    if n1 == 0
        plywriter;
    else
        plyappend;
    end
    
    HeaderEditor;
end