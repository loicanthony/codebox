function[out,order]=ion(in,f)
for i = 1 : size(in,2)
    [fpx(i),~,~]=feval(f,in(:,i));
end
[~,idx] = sort(fpx);
order = fliplr(idx);
out = in(:,fliplr(idx));
