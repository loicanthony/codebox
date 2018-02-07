function[out,idx2]=iom(in,x,complete_history)

%Change le nom des variables compliqu�es et update les nombres necessaires
%a la construction du modele
% Il ne faut pas avoir deux fois le meme pt dans l'history. WTF imfil?

pts = complete_history.good_points';
[pts,subvector,~] = unique(pts,'rows');
pts = pts';
values = complete_history.good_values';
values = values(subvector)';
n= size(pts(:,1),1); %n le nombre de variables
q = (n+1)*(n+2)/2; % pour la base naturelle, q = nb de points pour le model, max 50
p = size(pts,2); % nombre de points dans la history

% Cas ou il n'y a meme pas assez de points pour faire juste une
% approximation lin�aire... comme dans nomad
if p < n+1
    out = in;
    idx2 = 1:size(in,2);
    return
end

%Construit un vecteur 2d qui dit pour chaque x_q, combien il y a de termes
%mixte
mat = ones(p,p);
matL = ones(p,n+1);
matQ = ones(p,(n*(n+1)/2));

if p >= q
    %trouver les points les plus pr�s de x et updater pts pour pts = pts au
    %nombre de q
    for i = 1:p
        distance(i) = norm(pts(:,i)-x);
    end
    [~,idx]=sort(distance);
    
    % On prends les points les plus pr�s
    
    pts = pts(:,idx(1:q));
    values = values(idx(1:q));
    
    mat = ones(q,q);
    matL = ones(q,n+1);
    matQ = ones(q,(n*(n+1)/2));
    p=q;
end

nb_term_mix = (n+1)*(n+2)/2-1-2*n;

% Cette matrice permets de trouver combien de termes mixtes il y a
mat_idx = triu(ones(n)-eye(n));

line1 = [];
line2 = [];
for i = 1 : n
    [is1,idx]=find(mat_idx(i,:)==1);
    line1 = [line1 i*is1];
    line2 = [line2 idx];
end


mat_tm = [line1;line2];

% Initialization incluant termes constants

% Termes lin�aires
for i = 1 : n
    mat(:,i+1) = pts(i,:)';
    matL(:,i+1) = pts(i,:)';
    mat(:,i+n+1) = pts(i,:).^2' / 2;
    matQ(:,i) =  pts(i,:).^2' / 2;
end

% Termes quadratiques
for i = 1 : nb_term_mix
    mat(:,i+2*n+1) = pts(mat_tm(1,i),:) .* pts(mat_tm(2,i),:);
    matQ(:,n+i)= pts(mat_tm(1,i),:) .* pts(mat_tm(2,i),:);
end

% Construction de la matrice F
F = [matQ*matQ' matL;matL' zeros(size(matL',1),size(matL,2))];
% Si la matrice est singuliere on ordonne jamais
% if abs(det(F))>0.0001
% mualphaL = linsolve(F,[values';zeros(n+1,1)]);
mualphaL = F\[values';zeros(n+1,1)];
mu = mualphaL(1:p);
alphaL = mualphaL(p+1:end);

alphaQ = matQ'*mu;
alpha = [alphaL;alphaQ];

% Construction de phi des points en entr�
x_size = size(in,2);
phi_x = ones(q,x_size);
for j = 1 : x_size
    for i = 1 : n
        phi_x(i+1,j) = in(i,j);
        phi_x(i+n+1,j) = in(i,j).^2' / 2;
    end
    for i = 1 : nb_term_mix
        phi_x(i+2*n+1,j) = in(mat_tm(1,i),j) .* in(mat_tm(2,i),j);
    end
end

% On resouds le systeme
mf_x = alpha'*phi_x;

% % Trace un graphe pour voir
%x = linspace(0,10);
%y = linspace(0,10);
%[X,Y] = meshgrid(x,y);

%for i = 1 : 100
%    for j = 1 : 100
%        Z(i,j) = alpha'*phi([X(i,j);Y(i,j)]);
%    end
%end


% On ordonne
[~,idx2]=sort(mf_x);
out = in(:,idx2);


end