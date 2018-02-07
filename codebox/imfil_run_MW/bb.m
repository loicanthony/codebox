function [fv,ifail,icount]=bb(x)
% La fonction � optimiser.

% Nom al�atoire pour un fichier
symbols = ['a':'z' 'A':'Z' '0':'9'];
MAX_ST_LENGTH = 10;
stLength = randi(MAX_ST_LENGTH)+6;
nums = randi(numel(symbols),[1 stLength]);
filename = symbols (nums);
filename = [filename '.txt'];

% xtest pour tester le print dans le pt.
% xtest = [1;2;3;4;5;6;7;8;9];

% G�n�rer un fichier .txt avec le point x � l'interieur
fileID = fopen(filename,'w');
fprintf(fileID,'%d ',x');
fclose(fileID);
[ifail,fv] = system(['./bb.exe ' filename]);
icount = 1;
fv = str2num(fv);
delete(filename)
if isempty(fv)
    ifail = 1;
    fv = NaN;
end
if fv == Inf
    ifail = 1;
    fv = NaN;
end


%end