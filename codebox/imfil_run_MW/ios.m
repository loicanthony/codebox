function[out,order]=ios(in,x,complete_history)
% this is ordering with the last success direction.
% I can't really use this one but, I could always use data from
% complete_history to compute another similar direction
if size(complete_history.good_values,2) < 2
    out = in;
    order = 1:size(in,2);
    return
end
minval = find(complete_history.good_values == min(complete_history.good_values));
others = find(complete_history.good_values ~= min(complete_history.good_values));

if (ismember(x',(complete_history.good_points(:,minval))','rows'))
    % alors le point minimal est le point courant, on doit le deleter et
    % retrouver un autre minimum
    temp_hist = complete_history.good_points(:,others);
    temp_vals = complete_history.good_values(:,others);
    minval2 = find(temp_vals == min(temp_vals)); % donne l'indice du min
    minpoint =temp_hist(:,minval2);
    minpoint=minpoint(:,1);
    vector = x-minpoint;
else
    minpoint = complete_history.good_points(:,minval);
    vector = minpoint-x;
end

for i = 1 : size(in,2)
    norms(i) = norm(in(:,i));
    cosses(i) = vector'*in(:,i)/norms(i)/norm(vector);
end
[~,idx] = sort(cosses);
order = fliplr(idx);
out = in(:,fliplr(idx));
end
