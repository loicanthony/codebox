function[out]=phi(in)
% Cette matrice permets de trouver combien de termes mixtes il y a
n = length(in);
q=(n+1)*(n+2)/2;
mat_idx = triu(ones(n)-eye(n));
nb_term_mix = (n+1)*(n+2)/2-1-2*n;

%Construit un vecteur 2d qui dit pour chaque x_q, combien il y a de termes
%mixte
line1 = [];
line2 = [];
for i = 1 : n
    [is1,idx]=find(mat_idx(i,:)==1);
    line1 = [line1 i*is1];
    line2 = [line2 idx];
end
mat_tm = [line1;line2];
out = ones(q,1);
% Termes linéaires quadratique aps mixte
for i = 1 : n
    out(i+1) = in(i);
    out(i+n+1) = in(i).^2' / 2;
end

% Termes quadratiques mixtes
for i = 1 : nb_term_mix
    out(i+2*n+1) = in(mat_tm(1,i)) .* in(mat_tm(2,i));
end

end