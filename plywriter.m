pclSize = pcCount;

% Create ply file
fileID = fopen('matply.ply','w');

% Write the file header. \r\n moves to the next line.
fprintf(fileID,'ply\r\n');
fprintf(fileID,'format ascii 1.0\r\n');
fprintf(fileID,'element vertex %5d\r\n',pclSize); % How to overwrite this?
fprintf(fileID,'property float32 x\r\n');
fprintf(fileID,'property float32 y\r\n');
fprintf(fileID,'property float32 z\r\n');
fprintf(fileID,'end_header\r\n');                                   

% Write initial coordinate set to ply file below header
for i = 1:pclSize-1
    fprintf(fileID,'%d %d %d\r\n',pcLineCropped(:,i));
end

% Last of coordinate set (separate from loop because no space at EOF)
fprintf(fileID,'%d %d %d',pcLineCropped(:,pclSize));

%fprintf(fileID,'\r\ncomment testing123 testing123');    

fclose(fileID);

prevTotal = pclSize;

% Once this program is finished, run RotMat.m