% The following values will be used once a method of autocropping is made

% y1Crop =
% y2Crop =
% zDisplacement =
imread(strcat(s1,'%d',s2)
%% Laser Profile Scan
%s1 = 'buddha'; s2 = sprintf('%d',a); s3 = '.jpg';
%filename = strcat(s1,s2,s3);

if n1 == 0
    img = imread('buddha2.jpg');
    img = imrotate(img,180); %Rotation is to help translate image space to 3d space
end

pcLine = zeros(3,500);
pcCount = 0;

%Currently, only manual cropping is available. Display flipped raw image
%and specify max and min Y values.
start = 740;                                 %"start" is the pixel row where the scan begins
%stop = length(LProfile(:,1,1));             %"stop" is the loop's ending point 
stop = 1560;
inc = 10;                                    %"inc" is the # of rows by which the scan jumps s.t. not all rows need to be scanned


for lineNum = start:inc:stop

    % f is a single row (indexed as lineNum) of the image's red pixels
    % This line moves down the image by 'inc' each loop
    f = uint8(zeros(1,length(img(1,:,1))));
    f(1,:) = img(lineNum,:,1);

    % Find maximum of designated pixel row
    [Y,Ii] = max(f);
    
    % If max brightness is above threshold, store as point in pointcloud
    if Y > 50
        pcCount = pcCount+1;
        pcLine(:,pcCount) = [Ii,0,lineNum] ;
    end

end

% Now that # of significant points is known, crop the pcLine data structure
pcLineCropped = zeros(3,pcCount);

for x = 1:pcCount
    pcLineCropped(:,x) = pcLine(:,x);
end  

pcLineCropped(1,:) = pcLineCropped(1,:)-2000; %2000 is displacement from z-axis in this case

theta = n1;
R = [cos(theta) -sin(theta) 0;
     sin(theta)  cos(theta) 0;
     0        0      1];

pcLineCropped=R*pcLineCropped;

% Plot all points in cropped line structure
%plot3(pcLineCropped(1,:),pcLineCropped(2,:),pcLineCropped(3,:))

% Once this program is finished, run plywriter.m
