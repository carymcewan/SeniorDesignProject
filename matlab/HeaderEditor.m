% The sole purpose of this file is to update the header's third line to the 
% new number of verticies every time a new line is obtained

replaceLine = 3;
myformat = 'element vertex %5d\r\n';
vertexNum = prevTotal; % Make this a formula that adds the appropriate number of verticies for each scan

fileID = fopen('matply.ply','r+');

for k=1:(replaceLine-1);
   fgetl(fileID);
end

fseek(fileID,0,'cof');

fprintf(fileID, myformat, vertexNum);
fclose(fileID);