problist = 1:53;
typelist = {'SMOOTH','NONDIFF','WILD3','NOISY3'};
typenum = containers.Map;
typenum('SMOOTH')=1;
typenum('NONDIFF')=2;
typenum('WILD3')=3;
typenum('NOISY3')=4;
ordolist = ['r','l','o','s','n','m'];
load('bound_data')
global ordo;

% Compile le programme pour trouver x0
% !g++ -o generate_x0.exe generate_x0.cpp
% for np = 1 : 52
%   for tp = 1 :4
% end
for no = 1:3 % juste random et lexico
    for np = 1 :53
        for tp = 1:4
            for seed = 1:10
                ordo = ordolist(no); % Pour l'ordonnancement, comment out si on le veut pas
                disp(strjoin(['prob ' string(np) ' style ' typelist{tp} ' seed ' string(seed) '\n' ordolist(no)]))
                type = typelist{tp};
                dataindex = (np-1)*4 +tp -1;

                %Genere la blackbox
                npstring = num2str(np);
                system(['python bb_maker.py ' npstring ' ' type]);
                pause(3)

                % ici on trouve les bornes avec np et bound_data
                iterator = 3;
                a = [];

                % On prends les valeurs existante dans la ligne de bound_data pour le prob
                % correspondant
                while isempty(bound_data{(np-1)*4 +tp,iterator}) == false
                    a = [a, str2num(bound_data{(np-1)*4 +tp,iterator})];
                    iterator = iterator +1;
                end

                % On prends la dimensionjava.io.FileNotFoundException: /home/sarrloic/.matlab/R2017b/History.xml (Trop de fichiers ouverts)

                dim=length(a)/2;

                % On prends le fix du log base 10 du plus grand entre la solution et le pt
                % initial et on centre � 0.
                bnds = 10^(fix(log10(max(abs(a))))+1);
                bounds = zeros(dim,2);
                bounds(:,1) = -bnds;
                bounds(:,2) =bnds;

                % D�termine le point de d�part (redondant mais fait avant bounds)
                % system(['g++ generate_x0.cpp -o generate_x0.exe']);
                [ifail,x0] = system(['./generate_x0.exe ' num2str(np)]);
                x0=str2num(x0)';

                % Budget de 1500 comme NOMAD, � changer?
                budget=1500;

                %Roule l'algorithme avec case 1 = random
                %ordo = 'o';
                % [x,histout,comp]=imfil(x0,'bb',budget,bounds,imfil_optset());
                options = imfil_optset;
                options = imfil_optset('stencil_wins',1,options);
                [x,histout,comp]=imfil_modified_failures(x0,'bb',budget,bounds,options);

                % Fa�on d'afficher les r�sultats pris de l'exemple 
                res = zeros(length(comp.good_values(1,:)), dim+1);
                for i = 1 : length(comp.good_values(1,:))
                    res(i,:) = [comp.good_points(:,i)' comp.good_values(i)];
                end
                
                % Nom du fichier à sauvegarder
                % filepath = ['results/' num2str(problist(np)) '_' num2str(typelist{tp}) '/n/'];
                filepath = ['results/' num2str(problist(np)) '_' num2str(typelist{tp}) '/o' ordolist(no) '/'];
                % Nom du file pour ordonnancement nul sans opportunisme
                % filename = [num2str(problist(np)) '_' typelist{tp} '_history_' num2str(seed(1)) '_in.txt'];
                % Nom du file pour ordonnancements avec opportunisme
                filename = [num2str(problist(np)) '_' typelist{tp} '_history_' num2str(seed(1)) '_io' ordolist(no) '.txt'];
                dlmwrite([filepath filename],res,'Delimiter',' ');
                fclose('all')
            end
        end
    end
end