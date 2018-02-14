problist = 1:53;
typelist = {'SMOOTH','NONDIFF','WILD3','NOISY3'};
typenum = containers.Map;
typenum('SMOOTH')=1;
typenum('NONDIFF')=2;
typenum('NOISY3')=4;
ordolist = ['r','l','n','m','s','o'];
load('bound_data')
global ordo
tps = [1];

for np = 43:53
    for tp = tps
        type = typelist{tp};
        dataindex = (np-1)*4 +tp -1;

        %Genere la blackbox
        npstring = num2str(np);
        system(['python bb_maker.py ' npstring ' ' type]);
        pause(2)


        % ici on trouve les bornes avec np et bound_data
        iterator = 3;
        a = [];

        % On prends les valeurs existante dans la ligne de bound_data pour le prob
        % correspondant
        while isempty(bound_data{(np-1)*4 +tp,iterator}) == false
        a = [a, str2num(bound_data{(np-1)*4 +tp,iterator})];
        iterator = iterator +1;
        end
        % Calcul la bb au meilleurs pts

        % On prends la dimension et on trouve les meilleurs et ini values
        dim=length(a)/2;
        bb_ini = bb(a(1:dim));
        bb_best = bb(a(dim+1:2*dim));
        %scaledepth = max(7,floor(log2((bb_ini-bb_best)/bb_best)));
        scaledepth = 20;
        budget = 1000*(dim+1);
        % On prends le fix du log base 10 du plus grand entre la solution et le pt
        % initial et on centre � 0.
        bnds = 10^(fix(log10(max(abs(a)))));
        bounds = zeros(dim,2);
        bounds(:,1) = -bnds;
        bounds(:,2) =bnds;
        if max(abs(a)) > max(bounds(:,2))
            bounds = 10*bounds;
        end

        % D�termine le point de d�part (redondant mais fait avant bounds)
        % system(['g++ generate_x0.cpp -o generate_x0.exe']);
        [ifail,x0] = system(['./generate_x0.exe ' num2str(np)]);
        x0=str2num(x0)';

        for no =2:2
            % Stand alone paramsbb
%                 np = 39;
%                 tp = 1;
%                 seed = 1; 
%                 no = 1;
            ordo = ordolist(no);
           % fprintf(fopen('log.txt','a+'),' %s \n',(strjoin(['prob ' string(np) ' style ' typelist{tp} ' seed ' string(seed) '\n' ordolist(no)])));

            % Roule l'algorithme avec case 1 = random
            % [x,histout,comp]=imfil_modified(x0,'bb',budget,bounds,imfil_optset());

            % Roule l'algorithme avec random mais aussi la version modifiée de
            % imfil_modified, soit celle avec les echecs forcés en cas de reussite
            options = imfil_optset;
            options = imfil_optset('stencil_wins',1,'scaledepth',scaledepth,options);
            [x,histout,comp]=imfil_modified_failures(x0,'bb',budget,bounds,options);

            % Fa�on d'afficher les r�sultats pris de l'exemple 
            % res = zeros(length(comp.good_values(1,:)), dim+1);
            res = zeros(1,dim+1);
            i=1;
            j=1;
            while i ~= length(comp.good_values(1,:))
                if ismember([comp.good_points(:,i)' comp.good_values(i)],res,'rows') == false
                    res(j,:) = [comp.good_points(:,i)' comp.good_values(i)];
                    j=j+1;
                end
                i=i+1;
            end

            % Nom du fichier à sauvegarder
            % filepath = ['results/' num2str(problist(np)) '_' num2str(typelist{tp}) '/n/'];
            filepath = ['results/' num2str(problist(np)) '_' num2str(typelist{tp}) '/o' ordolist(no) '/'];
            % Nom du file pour ordonnancement nul sans opportunisme
            % filename = [num2str(problist(np)) '_' typelist{tp} '_history_' num2str(seed(1)) '_in.txt'];
            % Nom du file pour ordonnancements avec opportunisme
            for seed = 1:10
                filename = [num2str(problist(np)) '_' typelist{tp} '_history_' num2str(seed) '_io' ordolist(no) '.txt'];
                dlmwrite([filepath filename],res,'Delimiter',' ');
                fclose('all');
            end
            clc
        end
    end
end