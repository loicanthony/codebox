function[out,order]=iol(in)
[out,order] = sortrows(in');
out=out';
order=order';
%     %This is lexicographic ordering
%     [l n] = size(in); % l = longueur du vecteur point, n = quantite de vecteurs points
%     entry = in;
%     %moved{1:amount}=0
%     for i = 1:n-1
%         for j = i+1:n % en regardant juste ceux apres je skip les permutations entre deux points déja un en avant de l'autre
%                 %Fabriquer vecteur comparaison
%                 %comp(1:l)=0;
%             for k = 1 : l
%                 if in(k,j) == in(k,i)
%                     %comp(k)=1;
%                 elseif in(k,j)>= in(k,i)
%                     %comp(k) = 2;
%                     break
%                 else
%                     %comp(k)=0;
%                     stash = in(:,j);
%                     in(:,j)=in(:,i);
%                     in(:,i)=stash;
%                     break
%                 end
%             end
%         end
%     end
%     out = in;
%     for a = 1 : size(out)
%         for b = 1 : size(out)
%             if entry(a) == out(
%     end
end
