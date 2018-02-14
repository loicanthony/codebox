function[out,permut]=ior(in)
% This is random ordering
    [~,n] = size(in);
    permut = randperm(n);
    out = in(:,permut);
end