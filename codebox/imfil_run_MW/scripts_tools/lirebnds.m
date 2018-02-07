id=fopen('imfil_bounds.txt', 'rt');
scan = textscan(id,'%s','Delimiter','\n');
fclose(id);
for i = 1 : length(scan{1})
    a=textscan(scan{1}{i},'%s');
    length(a{1})
    for j = 1:length(a{1})
        bound_data{i,j} = a{1}{j};
    end
end