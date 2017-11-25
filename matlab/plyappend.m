pclSize = pcCount;
prevTotal = pclSize + prevTotal;

% Open existing ply file for appending
fileID = fopen('matply.ply','a');  

% Move to next line
fprintf(fileID,'\r\n');

% Write newly rotated coordinate set to ply file below
for i = 1:pclSize-1
    fprintf(fileID,'%d %d %d\r\n',pcLineCropped(:,i));
end

fprintf(fileID,'%d %d %d',pcLineCropped(:,pclSize));

fclose(fileID);